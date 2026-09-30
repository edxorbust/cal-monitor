import { useState } from "react";
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
} from "../../components/Tracker/Tracker";

export default function Exercises() {
  const [date, setDate] = useState(today());
  const resource = useResource(`/activities/?date=${date}`, true);
  const action = useAction();
  const [form, setForm] = useState({
    name: "",
    duration: "",
    calories_burned: "",
  });
  const [editing, setEditing] = useState(null);
  const [message, setMessage] = useState("");
  const reset = () => {
    setForm({ name: "", duration: "", calories_burned: "" });
    setEditing(null);
  };
  const change = (key) => (e) => setForm({ ...form, [key]: e.target.value });
  const save = (e) => {
    e.preventDefault();
    setMessage("");
    action.run(async () => {
      const payload = {
        ...form,
        date,
        duration: Number(form.duration),
        calories_burned: Number(form.calories_burned),
      };
      if (editing) await api.patch(`/activities/${editing}/`, payload);
      else await api.post("/activities/", payload);
      reset();
      resource.reload();
      setMessage("Actividad guardada.");
    });
  };
  return (
    <Page
      title="Tu actividad"
      subtitle="Registra la duración y las calorías estimadas por ti o por tu dispositivo."
      date={date}
      onDate={(day) => {
        setDate(day);
        reset();
        setMessage("");
      }}
    >
      <div className="grid">
        <section className="panel">
          <h2>{editing ? "Editar actividad" : "Registrar actividad"}</h2>
          <form onSubmit={save}>
            <Field
              label="Actividad"
              maxLength={100}
              value={form.name}
              onChange={change("name")}
              required
            />
            <Field
              label="Duración (minutos)"
              type="number"
              min="1"
              max="1440"
              value={form.duration}
              onChange={change("duration")}
              required
            />
            <Field
              label="Calorías quemadas (kcal)"
              type="number"
              min="0"
              max="100000"
              step="any"
              value={form.calories_burned}
              onChange={change("calories_burned")}
              required
            />
            <Notice error>{action.error}</Notice>
            <Notice>{message}</Notice>
            <div className="actions">
              <button className="primary" disabled={action.busy}>
                {action.busy ? "Guardando…" : "Guardar actividad"}
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
          <h2>Actividad del día</h2>
          <ResourceState resource={resource} />
          {!resource.loading &&
            !resource.error &&
            (!resource.data?.length ? (
              <Empty>Aún no hay actividad para esta fecha.</Empty>
            ) : (
              resource.data.map((item) => (
                <div className="row" key={item.id}>
                  <div>
                    <strong>{item.name}</strong>
                    <p>
                      {item.duration} min · {number(item.calories_burned)} kcal
                    </p>
                  </div>
                  <div className="row-actions">
                    <button
                      className="text-button"
                      disabled={action.busy}
                      onClick={() => {
                        setForm({
                          name: item.name,
                          duration: item.duration,
                          calories_burned: item.calories_burned,
                        });
                        setEditing(item.id);
                        setMessage("");
                      }}
                    >
                      Editar
                    </button>
                    <DeleteButton
                      disabled={action.busy}
                      onClick={() =>
                        action.run(async () => {
                          await api.delete(`/activities/${item.id}/`);
                          if (editing === item.id) reset();
                          resource.reload();
                          setMessage("Actividad eliminada.");
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
