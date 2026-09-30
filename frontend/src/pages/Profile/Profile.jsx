import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../auth/context";
import api from "../../api/api";
import useResource from "../../hooks/useResource";
import useAction from "../../hooks/useAction";
import {
  Page,
  Field,
  Notice,
  ResourceState,
} from "../../components/Tracker/Tracker";

export default function Profile() {
  const profile = useResource("/profile/");
  const action = useAction();
  const { logout } = useContext(AuthContext);
  const [form, setForm] = useState(null);
  const [saved, setSaved] = useState(false);
  useEffect(() => {
    if (profile.data) setForm(profile.data);
  }, [profile.data]);
  const change = (key) => (e) => {
    setSaved(false);
    setForm({ ...form, [key]: e.target.value });
  };
  const save = (e) => {
    e.preventDefault();
    setSaved(false);
    action.run(async () => {
      const payload = {
        name: form.name,
        goal: form.goal,
        daily_calorie_goal: Number(form.daily_calorie_goal),
        water_goal_ml: Number(form.water_goal_ml),
      };
      for (const key of ["weight", "height", "goal_weight"])
        payload[key] =
          form[key] === "" || form[key] === null ? null : Number(form[key]);
      const { data } = await api.patch("/profile/", payload);
      setForm(data);
      setSaved(true);
    });
  };
  return (
    <Page
      title="Tu perfil y tus metas"
      subtitle="Un punto de partida que puedes ajustar cuando quieras."
    >
      <ResourceState resource={profile} />
      {form && !profile.loading && !profile.error && (
        <form onSubmit={save}>
          <div className="grid">
            <section className="panel">
              <h2>Sobre ti</h2>
              <p>
                Cuenta: {form.username} · {form.email}
              </p>
              <Field
                label="Nombre"
                value={form.name}
                onChange={change("name")}
                maxLength={100}
                required
              />
              <div className="split">
                <Field
                  label="Peso actual (kg)"
                  type="number"
                  min="1"
                  max="600"
                  step="0.1"
                  value={form.weight ?? ""}
                  onChange={change("weight")}
                />
                <Field
                  label="Altura (cm)"
                  type="number"
                  min="30"
                  max="300"
                  step="0.1"
                  value={form.height ?? ""}
                  onChange={change("height")}
                />
              </div>
              <button
                type="button"
                className="text-button danger"
                onClick={logout}
              >
                Cerrar sesión
              </button>
            </section>
            <section className="panel">
              <h2>Metas diarias</h2>
              <p>
                Los valores iniciales son editables. Elige tus propias metas.
              </p>
              <label className="field">
                Objetivo
                <select value={form.goal} onChange={change("goal")}>
                  <option value="">Sin definir</option>
                  <option value="M">Mantener peso</option>
                  <option value="P">Perder peso</option>
                  <option value="G">Ganar peso</option>
                </select>
              </label>
              <Field
                label="Peso meta (kg)"
                type="number"
                min="1"
                max="600"
                step="0.1"
                value={form.goal_weight ?? ""}
                onChange={change("goal_weight")}
              />
              <div className="split">
                <Field
                  label="Calorías (kcal/día)"
                  type="number"
                  min="1"
                  max="20000"
                  value={form.daily_calorie_goal}
                  onChange={change("daily_calorie_goal")}
                  required
                />
                <Field
                  label="Agua (ml/día)"
                  type="number"
                  min="1"
                  max="20000"
                  value={form.water_goal_ml}
                  onChange={change("water_goal_ml")}
                  required
                />
              </div>
            </section>
          </div>
          <Notice error>{action.error}</Notice>
          {saved && <Notice>Perfil y metas guardados.</Notice>}
          <button className="primary" disabled={action.busy}>
            {action.busy ? "Guardando…" : "Guardar perfil y metas"}
          </button>
        </form>
      )}
    </Page>
  );
}
