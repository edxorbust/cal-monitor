import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/api";
import { today, number } from "../../api/tracker";
import useResource from "../../hooks/useResource";
import useAction from "../../hooks/useAction";
import {
  Page,
  Field,
  Notice,
  ResourceState,
  Empty,
  DeleteButton,
  Stat,
} from "../../components/Tracker/Tracker";

export default function Dashboard() {
  const [date, setDate] = useState(today());
  const summary = useResource(`/summary/?date=${date}`);
  const meals = useResource(`/meals/?date=${date}`, true);
  const water = useResource(`/water/?date=${date}`, true);
  const action = useAction();
  const [amount, setAmount] = useState(250);
  const addWater = (value) =>
    action.run(async () => {
      await api.post("/water/", { amount: Number(value), date });
      water.reload();
      summary.reload();
    });
  const data = summary.data;
  return (
    <Page
      title="Tu resumen diario"
      subtitle="Registro de tu día a día."
      date={date}
      onDate={setDate}
    >
      <ResourceState resource={summary} />
      {data && !summary.loading && !summary.error && (
        <>
          <div className="stats">
            <Stat
              label="Consumidas"
              value={number(data.consumed)}
              unit="kcal"
            />
            <Stat label="Quemadas" value={number(data.burned)} unit="kcal" />
            <Stat label="Balance neto" value={number(data.net)} unit="kcal" />
            <Stat
              label={data.remaining >= 0 ? "Restantes" : "Sobre tu meta"}
              value={number(Math.abs(data.remaining))}
              unit="kcal"
              tone="accent"
            />
          </div>
          <p className="subtle">
            Meta: {number(data.calorie_goal)} kcal · Restantes = meta −
            consumidas + quemadas.{" "}
            <Link className="inline-link" to="/profile">
              Ajustar metas
            </Link>
          </p>
        </>
      )}
      <div className="grid">
        <section className="panel">
          <h2>Agua</h2>
          {data && !summary.loading && !summary.error && (
            <>
              <strong>
                {number(data.water_ml)} / {number(data.water_goal_ml)} ml
              </strong>
              <progress
                aria-label="Progreso de agua"
                value={Math.min(data.water_ml, data.water_goal_ml)}
                max={data.water_goal_ml}
              />
            </>
          )}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              addWater(amount);
            }}
          >
            <Field
              label="Cantidad de agua (ml)"
              type="number"
              min="1"
              max="10000"
              step="any"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
            <div className="actions">
              <button className="primary" disabled={action.busy}>
                Registrar agua
              </button>
              <button
                type="button"
                disabled={action.busy}
                onClick={() => addWater(250)}
              >
                + 250 ml
              </button>
              <button
                type="button"
                disabled={action.busy}
                onClick={() => addWater(500)}
              >
                + 500 ml
              </button>
            </div>
          </form>
          <Notice error>{action.error}</Notice>
          <ResourceState resource={water} />
          {!water.loading &&
            !water.error &&
            (!water.data?.length ? (
              <Empty>No has registrado agua para esta fecha.</Empty>
            ) : (
              water.data.map((item) => (
                <div className="row" key={item.id}>
                  <strong>{number(item.amount)} ml</strong>
                  <DeleteButton
                    disabled={action.busy}
                    onClick={() =>
                      action.run(async () => {
                        await api.delete(`/water/${item.id}/`);
                        water.reload();
                        summary.reload();
                      })
                    }
                  />
                </div>
              ))
            ))}
        </section>
        <section className="panel">
          <h2>Comidas del día</h2>
          <ResourceState resource={meals} />
          {!meals.loading &&
            !meals.error &&
            (!meals.data?.length ? (
              <Empty>Tu diario está vacío. Registra tu primera comida.</Empty>
            ) : (
              meals.data.map((meal) => (
                <div className="row" key={meal.id}>
                  <strong>{meal.name}</strong>
                  <span>{number(meal.calories)} kcal</span>
                </div>
              ))
            ))}
          <p>
            <Link className="inline-link" to="/food">
              Registrar o editar comidas →
            </Link>
          </p>
          <p>
            <Link className="inline-link" to="/exercises">
              Registrar actividad →
            </Link>
          </p>
        </section>
      </div>
    </Page>
  );
}
