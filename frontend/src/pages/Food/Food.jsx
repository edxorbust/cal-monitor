import React from "react";
import styles from "./Food.module.css";
import Navbar from "../../components/Navbar/Navbar";
import MenuBar from "../../components/MenuBar/MenuBar";
import ItemCardList from "../../components/ItemCardList/ItemCardList";

function Food() {
  const menuItems = [
    { label: "Hoy", path: "/food/hoy" },
    { label: "Esta Semana", path: "/food/semana" },
    { label: "Historial", path: "/food/historial" },
  ];

  const foodItems = [
    { id: 1, name: "Seco de carne", calories: 900, iconClass: "meat" },
    { id: 2, name: "Fideos", calories: 200, iconClass: "bowl-noodles" },
    { id: 3, name: "Carne asada", calories: 700, iconClass: "meat" },
  ];

  return (
    <>
      <div className={styles.mainContainer}>
        <h2>Comida</h2>
        <MenuBar items={menuItems} />
        <ItemCardList items={foodItems} unit="cal" />
      </div>
      <div className={styles.addButton}>+</div>
      <Navbar />
    </>
  );
}

export default Food;
