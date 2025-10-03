import React, { useEffect, useState } from "react";
import api from "../../api/api";
import { useNavigate } from "react-router-dom";
import styles from "./Dashboard.module.css";
import Navbar from "../../components/Navbar/Navbar";

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();


  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/login");
  };

  return (
  <>
    <div className={styles.mainContainer}>
      <h2>Dashboard</h2>
      <h3 className={styles.h2LeftAlign}>Calorias</h3>
      <div className={styles.containerFlex}>
        <div className={styles.containerCard}>
          <div className={styles.titleCard}>Consumidas</div>
          <div className={styles.titleCardBold}>0</div>
        </div>
        <div className={styles.containerCard}>
          <div className={styles.titleCard}>Quemadas</div>
          <div className={styles.titleCardBold}>0</div>
        </div>
      </div>
      <div>
          <div className={styles.containerFlexMidSpace}>
            <div className={styles.titleWater}>
            Restantes diarias:
            </div>
            <div className={styles.titleWater}>
            200
            </div>
          </div>
          <div className={styles.orangeGradientCaloriesLevel}>
          </div>   
      </div>
      <h3 className={styles.h2LeftAlign}>Agua</h3>
      <div>
        <div className={styles.containerFlexMidSpace}>
          <div className={styles.titleWater}>
            Litros diarios consumidos:
          </div>
          <div className={styles.titleWater}>
            1.3 L
          </div>
        </div>
        <div className={styles.blueGradientWaterLevel}>
        </div>
      </div>
      <h3 className={styles.h2LeftAlign}>Comida</h3>
      <div className={styles.containerFlexLeft}>
        <div className={styles.iconBox}>
          <i class='bx  bx-meat'  ></i> 
        </div>
        <div className={styles.exerciseDescriptionBox}>
          <div className={styles.titleWater}>Seco de carne</div>
          <div className={styles.exerciseTimeFont}>900 cal</div>
        </div>
      </div>
      <div className={styles.containerFlexLeft}>
        <div className={styles.iconBox}>
          <i class='bx  bx-bowl-noodles'  ></i>   
        </div>
        <div className={styles.exerciseDescriptionBox}>
          <div className={styles.titleWater}>Fideos</div>
          <div className={styles.exerciseTimeFont}>200 cal</div>
        </div>
      </div>
      <div className={styles.containerFlexLeft}>
        <div className={styles.iconBox}>
          <i class='bx  bx-meat'  ></i> 
        </div>
        <div className={styles.exerciseDescriptionBox}>
          <div className={styles.titleWater}>Carne asada</div>
          <div className={styles.exerciseTimeFont}>700 cal</div>
        </div>
      </div>
      <div className={styles.plusButton}>
            +
      </div>
      <h3 className={styles.h2LeftAlign}>Ejercicios</h3>
      <div className={styles.containerFlexLeft}>
        <div className={styles.iconBox}>
          <i class='bx  bx-running'  ></i> 
        </div>
        <div className={styles.exerciseDescriptionBox}>
          <div className={styles.titleWater}>Morning Run</div>
          <div className={styles.exerciseTimeFont}>30 min</div>
        </div>
      </div>
      <div className={styles.containerFlexLeft}>
        <div className={styles.iconBox}>
          <i class='bx  bx-dumbbell'  ></i>  
        </div>
        <div className={styles.exerciseDescriptionBox}>
          <div className={styles.titleWater}>Entrenamiento con pesas</div>
          <div className={styles.exerciseTimeFont}>45 min</div>
        </div>
      </div>
      <div className={styles.containerFlexLeft}>
        <div className={styles.iconBox}>
          <i class='bx  bx-dumbbell'  ></i>  
        </div>
        <div className={styles.exerciseDescriptionBox}>
          <div className={styles.titleWater}>Entrenamiento con pesas</div>
          <div className={styles.exerciseTimeFont}>45 min</div>
        </div>
      </div>
      <div className={styles.plusButton}>
            +
      </div>
    </div>
    <Navbar />
  </>
  );
}

export default Dashboard;