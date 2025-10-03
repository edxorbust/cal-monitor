import React from "react";
import styles from "./Profile.module.css";
import Navbar from "../../components/Navbar/Navbar";
import WeightTrendChart from "../../components/WeightTrendChart/WeightTrendChart";
import ItemCardListGoals from "../../components/ItemCardListGoals/ItemCardListGoals";
import ItemCardListSettings from "../../components/ItemCardListSettings/ItemCardListSettings";

function Profile() {

  const goalsItems = [
    { id: 1, name: "Peso Meta", description: "180", unit: "lbs", iconClass: "body" },
    { id: 2, name: "Consumo calorico diario", description: "2000", unit: "cal", iconClass: "meat" },
    { id: 3, name: "Consumo de agua diario", description: "2", unit: "lts", iconClass: "water-drop" },
  ];

  const settingsItems = [
    { id: 1, name: "Notificaciones", iconClass: "bell" },
    { id: 2, name: "Privacidad", iconClass: "lock" },
    { id: 3, name: "Idioma", iconClass: "globe" },
    { id: 4, name: "Cerrar sesión", iconClass: "arrow-out-right-square-half" }
  ];

  return (
    <>
      <div className={styles.mainContainer}>
        <h2>Perfil</h2>
        <div className={styles.containerFlexColumn}>
          <div className={styles.userPicture}>
            <i class="bx  bx-user"></i>
          </div>
          <div>
            <h3 className={styles.h3margin}>Username</h3>
            <div className={styles.exerciseTimeFont}>Description</div>
            <div className={styles.exerciseTimeFont}>Description 2</div>
          </div>
        </div>
        <div className={styles.progressContainer}>
          <h4 className={styles.h4titleLeft}>Peso</h4>
          <div className={styles.weightContainer}>199 lb</div>
        </div>
        <WeightTrendChart />
        <div className={styles.progressContainer}>
          <h4 className={styles.h4titleLeft}>Metas</h4>
          <ItemCardListGoals items={goalsItems} />
        </div>
        <div className={styles.progressContainer}>
          <h4 className={styles.h4titleLeft}>Configuración</h4>
          <ItemCardListSettings items={settingsItems} />
        </div>
      </div>
      <Navbar />
    </>
  );
}

export default Profile;
