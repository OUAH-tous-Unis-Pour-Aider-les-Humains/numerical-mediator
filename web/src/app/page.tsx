import { GraphLoader } from "@/components/graph-loader";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <section className={styles.intro}>
          <h1>Prototype local de schéma connecté à PostgreSQL</h1>
          <p>
            Cette première version charge un schéma depuis la base, puis
            l&apos;affiche avec zoom (+/− ou molette) et déplacement (cliquer +
            glisser).
          </p>
        </section>
        <GraphLoader />
      </main>
    </div>
  );
}
