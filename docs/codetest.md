<!-- Tema de Highlight.js (puedes cambiar github-dark por otro) -->
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">

<!-- Core de Highlight.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<!-- Lenguajes que te interesan -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/sql.min.js"></script>

<script>
  // Aplica syntax highlighting a todos los <pre><code>
  hljs.highlightAll();
</script>

<style>
.code-explained {
  margin: 18px 0;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #1f2933;
  background: #020617;
  box-shadow:
    0 0 0 1px rgba(15, 23, 42, 0.25),
    0 12px 30px rgba(15, 23, 42, 0.55);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Header de la tarjeta */
.code-explained-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: radial-gradient(circle at top left, #0f172a 0, #020617 60%, #020617 100%);
  color: #e5e7eb;
  font-size: 0.86rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.4);
}

.code-explained-header i[py] {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  vertical-align: -3px;
}

.code-explained-header-main {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.code-explained-file {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.code-explained-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  opacity: 0.85;
}

.code-lang-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.18);
  color: #6ee7b7;
  font-size: 0.75rem;
}

.code-lang-pill::before {
  content: "🐍";
  font-size: 0.8rem;
}

.code-explained-links {
  display: flex;
  align-items: center;
  gap: 10px;
  white-space: nowrap;
}

.code-explained-header a {
  color: #93c5fd;
  text-decoration: none;
  font-size: 0.8rem;
}

.code-explained-header a:hover {
  text-decoration: underline;
}

/* Cuerpo */
.code-explained-body {
  padding: 10px 12px 12px;
}

/* Toolbar visual (no hace nada sin JS, es puramente estética) */
.code-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 6px;
}

.code-toolbar-btn {
  border: 0;
  padding: 2px 6px;
  border-radius: 999px;
  font-size: 0.7rem;
  background: rgba(148, 163, 184, 0.16);
  color: #e5e7eb;
}

/* Bloque de código: dejamos que highlight.js pinte los colores */
.code-explained-body pre {
  margin: 0;
  border-radius: 8px;
  background: #020617;
  font-size: 0.85rem;
}

/* Notas pedagógicas debajo */
.code-explained-notes {
  padding: 8px 12px 10px;
  background: #020617;
  border-top: 1px solid rgba(148, 163, 184, 0.35);
  font-size: 0.8rem;
  color: #e5e7eb;
}

.code-explained-notes ul {
  margin: 6px 0 0;
  padding-left: 18px;
}

.code-explained-notes li {
  margin: 2px 0;
}
</style>


<div class="code-explained">
  <div class="code-explained-header">
    <i py></i>
    <div class="code-explained-header-main">
      <div class="code-explained-file">
        website-morpion/models/game_repository.py
      </div>
      <div class="code-explained-meta">
        <span class="code-lang-pill">Python</span>
        <span>📍 Lignes 45–68</span>
      </div>
    </div>
    <div class="code-explained-links">
      <a href="../../website-morpion/models/game_repository.py">
        Voir le fichier
      </a>
      <a href="../../website-morpion/models/game_repository.py#L45-L68">
        ↗ Aller aux lignes 45–68
      </a>
    </div>
  </div>

  <div class="code-explained-body">
    <div class="code-toolbar">
      <button class="code-toolbar-btn">👁 Vue lecture</button>
      <button class="code-toolbar-btn">📋 Copy</button>
    </div>

    <pre><code class="language-python">
def get_game_by_id(game_id: int) -> dict:
    # ✏️ Récupère une partie spécifique depuis la base de données
    # Retourne toutes les informations utiles (équipes, plateau, règles)

    conn = get_db_connection()  # 🔗 Établit la connexion PostgreSQL
    cursor = conn.cursor()

    # 📊 Joint les tables parties, équipes et morpions
    query = """
        SELECT p.id, p.plateau, p.tour_actuel, p.statut,
               e1.nom AS equipe1, e2.nom AS equipe2,
               m.regles, m.taille
        FROM parties p
        JOIN equipes e1 ON p.equipe1_id = e1.id
        JOIN equipes e2 ON p.equipe2_id = e2.id
        JOIN morpions m ON p.morpion_id = m.id
        WHERE p.id = %s
    """

    cursor.execute(query, (game_id,))  # 🛡️ Paramètres =&gt; évite l'injection SQL
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result  # 📤 Dict ou None si la partie n'existe pas
    </code></pre>
  </div>

  <div class="code-explained-notes">
    <strong>Résumé pédagogique :</strong>
    <ul>
      <li>🔍 Un seul point d'accès pour récupérer une partie complète.</li>
      <li>🛡 Requête paramétrée pour se protéger contre l'injection SQL.</li>
      <li>🧹 Connexion fermée proprement (cursor + conn).</li>
    </ul>
  </div>
</div>
