import { GraphLoader } from "@/components/graph-loader";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <section className={styles.intro}>
          <h1>Prototype local de schéma (React Flow + PostgreSQL)</h1>
          <p>
            Cette version charge le dernier schéma en base et permet aussi de
            générer un nouveau graphe depuis un texte via Ollama en local.
          </p>
        </section>
        <GraphLoader />
      </main>
    </div>
  );
}
