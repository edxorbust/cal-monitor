import { useState } from "react";
import api from "../../api/api";
import { number } from "../../api/tracker";
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
const initial = { name: "", calories: "", portion_size: 100, unit: "g" };
export default function Ingredients() {
  const resource = useResource("/ingredients/", true);
  const action = useAction();
  const [form, setForm] = useState(initial);
  const [editing, setEditing] = useState(null);
  const [saved, setSaved] = useState("");
  const change = (key) => (e) => setForm({ ...form, [key]: e.target.value });
  const reset = () => {
    setForm(initial);
    setEditing(null);
  };
  const submit = (e) => {
    e.preventDefault();
    setSaved("");
    action.run(async () => {
      const payload = {
        ...form,
        calories: Number(form.calories),
        portion_size: Number(form.portion_size),
      };
      if (editing) await api.patch(`/ingredients/${editing}/`, payload);
      else await api.post("/ingredients/", payload);
      reset();
      resource.reload();
      setSaved("Ingrediente guardado. Ya puedes usarlo en tus comidas.");
    });
  };
  return (
    <Page
      title="Tus ingredientes"
      subtitle="Guarda la información de la etiqueta y calcula tus porciones."
    >
      <div className="grid">
        <section className="panel">
          <h2>{editing ? "Editar ingrediente" : "Nuevo ingrediente"}</h2>
          <form onSubmit={submit}>
            <Field
              label="Nombre del ingrediente"
              value={form.name}
              maxLength={100}
              onChange={change("name")}
              required
            />
            <div className="split">
              <Field
                label="Porción de referencia"
                type="number"
                min="0.01"
                max="100000"
                step="any"
                value={form.portion_size}
                onChange={change("portion_size")}
                required
              />
              <label className="field">
                Unidad
                <select value={form.unit} onChange={change("unit")}>
                  <option value="g">Gramos</option>
                  <option value="ml">Mililitros</option>
                  <option value="unidad">Unidades</option>
                </select>
              </label>
            </div>
            <Field
              label="Calorías de esa porción (kcal)"
              type="number"
              min="0"
              max="100000"
              step="any"
              value={form.calories}
              onChange={change("calories")}
              required
            />
            <Notice error>{action.error}</Notice>
            <Notice>{saved}</Notice>
            <div className="actions">
              <button className="primary" disabled={action.busy}>
                {action.busy ? "Guardando…" : "Guardar ingrediente"}
              </button>
              {editing && (
                <button type="button" onClick={reset}>
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </section>
        <section className="panel">
          <h2>Mi catálogo</h2>
          <ResourceState resource={resource} />
          {!resource.loading &&
            !resource.error &&
            (!resource.data?.length ? (
              <Empty>Aún no hay ingredientes. Añade el primero.</Empty>
            ) : (
              resource.data.map((item) => (
                <div className="row" key={item.id}>
                  <div>
                    <strong>{item.name}</strong>
                    <p>
                      {number(item.calories)} kcal / {number(item.portion_size)}{" "}
                      {item.unit}
                    </p>
                  </div>
                  <div className="row-actions">
                    <button
                      className="text-button"
                      disabled={action.busy}
                      onClick={() => {
                        setForm(item);
                        setEditing(item.id);
                        setSaved("");
                      }}
                    >
                      Editar
                    </button>
                    <DeleteButton
                      disabled={action.busy}
                      onClick={() =>
                        action.run(async () => {
                          await api.delete(`/ingredients/${item.id}/`);
                          if (editing === item.id) reset();
                          resource.reload();
                          setSaved(
                            "Ingrediente eliminado. Las comidas anteriores conservan sus calorías.",
                          );
                        })
                      }
                    />
                  </div>
                </div>
              ))
            ))}
        </section>
      </div>
    </Page>
  );
}
