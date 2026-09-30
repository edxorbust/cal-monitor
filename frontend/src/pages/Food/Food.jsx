import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/api";
import { number, today } from "../../api/tracker";
import useResource from "../../hooks/useResource";
import useAction from "../../hooks/useAction";
import {
  Page,
  Field,
  Notice,
  ResourceState,
  Empty,
  DeleteButton,
} from "../../components/Tracker/Tracker";

export default function Food() {
  const [date, setDate] = useState(today());
  const meals = useResource(`/meals/?date=${date}`, true);
  const catalog = useResource("/ingredients/", true);
  const action = useAction();
  const [name, setName] = useState("");
  const [calories, setCalories] = useState("");
  const [mode, setMode] = useState("manual");
  const [items, setItems] = useState([{ ingredient: "", quantity: "" }]);
  const [editing, setEditing] = useState(null);
  const [message, setMessage] = useState("");
  const reset = () => {
    setName("");
    setCalories("");
    setItems([{ ingredient: "", quantity: "" }]);
    setEditing(null);
  };
  const estimate = items.reduce((sum, item) => {
    const ingredient = catalog.data?.find(
      (i) => i.id === Number(item.ingredient),
    );
    return (
      sum +
      (ingredient
        ? (ingredient.calories * Number(item.quantity)) /
          ingredient.portion_size
        : 0)
    );
  }, 0);
  const changeItem = (index, key, value) =>
    setItems(
      items.map((item, i) => (i === index ? { ...item, [key]: value } : item)),
    );
  const save = (e) => {
    e.preventDefault();
    setMessage("");
    action.run(async () => {
      const payload = {
        name,
        date,
        ingredients:
          mode === "ingredients"
            ? items.map((item) => ({
                ingredient: Number(item.ingredient),
                quantity: Number(item.quantity),
              }))
            : [],
      };
      if (mode === "manual") payload.calories = Number(calories);
      if (editing) await api.patch(`/meals/${editing}/`, payload);
      else await api.post("/meals/", payload);
      reset();
      meals.reload();
      setMessage(
        "Comida guardada. El resumen diario se actualiza con este registro.",
      );
    });
  };
  const edit = (meal) => {
    setName(meal.name);
    setCalories(meal.calories);
    setEditing(meal.id);
    setMessage("");
    const fromIngredients =
      meal.items.length && meal.items.every((item) => item.ingredient);
    setMode(fromIngredients ? "ingredients" : "manual");
    setItems(
      fromIngredients
        ? meal.items.map((item) => ({
            ingredient: item.ingredient,
            quantity: item.quantity,
          }))
        : [{ ingredient: "", quantity: "" }],
    );
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  return (
    <Page
      title="Tus comidas"
      subtitle="Registra lo que comes. Las cantidades hacen la diferencia."
      date={date}
      onDate={(value) => {
        setDate(value);
        reset();
        setMessage("");
      }}
    >
      <div className="grid">
        <section className="panel">
          <h2>{editing ? "Editar comida" : "Registrar comida"}</h2>
          <form onSubmit={save}>
            <Field
              label="Nombre de la comida"
              placeholder="Ej. Almuerzo"
              maxLength={100}
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <label className="field">
              Cómo calcular las calorías
              <select value={mode} onChange={(e) => setMode(e.target.value)}>
                <option value="manual">Introducir calorías manualmente</option>
                <option value="ingredients">
                  Calcular con mis ingredientes
                </option>
              </select>
            </label>
            {mode === "manual" ? (
              <Field
                label="Calorías totales (kcal)"
                type="number"
                min="0"
                max="1000000"
                step="any"
                value={calories}
                onChange={(e) => setCalories(e.target.value)}
                required
              />
            ) : (
              <>
                <ResourceState resource={catalog} />
                {!catalog.loading &&
                  !catalog.error &&
                  !catalog.data?.length && (
                    <p>
                      Primero{" "}
                      <Link className="inline-link" to="/ingredients">
                        añade ingredientes a tu catálogo
                      </Link>
                      .
                    </p>
                  )}
                {items.map((item, index) => (
                  <div className="ingredient-line" key={index}>
                    <label className="field">
                      Ingrediente {index + 1}
                      <select
                        aria-label={`Ingrediente ${index + 1}`}
                        value={item.ingredient}
                        onChange={(e) =>
                          changeItem(index, "ingredient", e.target.value)
                        }
                        required
                      >
                        <option value="">Seleccionar</option>
                        {catalog.data?.map((ingredient) => (
                          <option key={ingredient.id} value={ingredient.id}>
                            {ingredient.name} ({ingredient.unit})
                          </option>
                        ))}
                      </select>
                    </label>
                    <Field
                      label={`Cantidad ${index + 1}`}
                      type="number"
                      min="0.01"
                      max="100000"
                      step="any"
                      value={item.quantity}
                      onChange={(e) =>
                        changeItem(index, "quantity", e.target.value)
                      }
                      required
                    />
                    <button
                      type="button"
                      aria-label={`Quitar ingrediente ${index + 1}`}
                      disabled={items.length === 1}
                      onClick={() =>
                        setItems(items.filter((_, i) => i !== index))
                      }
                    >
                      ×
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  disabled={items.length >= 100}
                  onClick={() =>
                    setItems([...items, { ingredient: "", quantity: "" }])
                  }
                >
                  + Otro ingrediente
                </button>
                <p className="badge">Total estimado: {number(estimate)} kcal</p>
                <p className="subtle">
                  La cantidad usa la unidad del ingrediente. El total definitivo
                  se calcula al guardar.
                </p>
              </>
            )}
            <Notice error>{action.error}</Notice>
            <Notice>{message}</Notice>
            <div className="actions">
              <button
                className="primary"
                disabled={
                  action.busy ||
                  (mode === "ingredients" &&
                    (catalog.loading ||
                      !!catalog.error ||
                      !catalog.data?.length))
                }
              >
                {action.busy ? "Guardando…" : "Guardar comida"}
              </button>
              {editing && (
                <button type="button" onClick={reset}>
                  Cancelar edición
                </button>
              )}
            </div>
          </form>
        </section>
        <section className="panel">
          <h2>Comidas del día</h2>
          <ResourceState resource={meals} />
          {!meals.loading && !meals.error && (
            <>
              <p className="badge">
                Total:{" "}
                {number(
                  meals.data?.reduce((sum, item) => sum + item.calories, 0),
                )}{" "}
                kcal
              </p>
              {!meals.data?.length ? (
                <Empty>No hay comidas para esta fecha.</Empty>
              ) : (
                meals.data.map((meal) => (
                  <div className="row" key={meal.id}>
                    <div>
                      <strong>{meal.name}</strong>
                      <p>{number(meal.calories)} kcal</p>
                      {meal.items.map((item, index) => (
                        <p key={index}>
                          {item.name} · {number(item.quantity)} {item.unit} ·{" "}
                          {number(item.calories)} kcal
                        </p>
                      ))}
                    </div>
                    <div className="row-actions">
                      <button
                        className="text-button"
                        disabled={action.busy}
                        onClick={() => edit(meal)}
                      >
                        Editar
                      </button>
                      <DeleteButton
                        disabled={action.busy}
                        onClick={() =>
                          action.run(async () => {
                            await api.delete(`/meals/${meal.id}/`);
                            if (editing === meal.id) reset();
                            meals.reload();
                            setMessage("Comida eliminada.");
                          })
                        }
                      />
                    </div>
                  </div>
                ))
              )}
            </>
          )}
        </section>
      </div>
    </Page>
  );
}
