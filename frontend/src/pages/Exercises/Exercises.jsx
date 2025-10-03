import React from "react";
import styles from "./Exercises.module.css";
import Navbar from "../../components/Navbar/Navbar";
import MenuBar from "../../components/MenuBar/MenuBar";
import ItemCardList from "../../components/ItemCardList/ItemCardList";

function Exercises() {
  const menuItems = [
    { label: "Hoy", path: "/exercises/hoy" },
    { label: "Esta Semana", path: "/exercises/semana" },
    { label: "Historial", path: "/exercises/historial" },
  ];

  const exerciseItems = [
    { id: 1, name: "Correr", calories: 300, time: 30, iconClass: "running" },
    { id: 2, name: "Nadar", calories: 400, time: 45, iconClass: "swimming" },
    { id: 3, name: "Pesas", calories: 500, time: 60, iconClass: "dumbbell" },
  ];

  return (
    <>
      <div className={styles.mainContainer}>
        <h2>Ejercicios</h2>
        <MenuBar items={menuItems} />
        <ItemCardList items={exerciseItems} unit="cal" />
      </div>

      <div className={styles.addButton}>+</div>
      <Navbar />
    </>
  );
}

export default Exercises;
