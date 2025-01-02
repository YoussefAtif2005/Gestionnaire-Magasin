import tkinter as tk
import customtkinter as ctk
import psycopg2

# Connexion à la base de données PostgreSQL (remplacer par vos identifiants de base de données)
conn = psycopg2.connect(
    dbname='COMMERCE', 
    user='postgres', 
    password='admin', 
    host='localhost', 
    port='5432'
)
cursor = conn.cursor()

# Initialisation de l'application customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class SQLQueryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ineterface graphique des requêtes SQL")
        self.geometry("800x600")

        # Options de requêtes
        self.query_label = ctk.CTkLabel(self, text="Sélectionner une requête :", font=("Arial", 16))
        self.query_label.pack(pady=10)

        self.query_var = tk.StringVar(value="1")
        self.query_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.query_var, 
            values=[
                "1. Nom et prix des produits",
                "2. Nombre de clients",
                "3. Moyenne des prix des produits",
                "4. Moyenne des salaires des commercents",
                "5. Clients ayant fait des achats récemment",
                "6. Top 10 produits les plus vendus",
                "7. Clients les plus fidèles",
                "8. Classement des commercents",
                "9. Nombre de ventes par produit et commercent",
                "10. Achats de chaque client par produit",
                "11. Chiffre d'affaire par commercent",
                "12. Commercents ayant vendu plus de 10 produits",
                "13. Mettre à jour salaire (prime)",
                "14. Mettre à jour remise clients",
                "15. Nombre de ventes par produit"
            ]
        )
        self.query_menu.pack(pady=10)

        # Bouton pour exécuter la requête
        self.execute_button = ctk.CTkButton(self, text="Exécuter la requête", command=self.execute_query)
        self.execute_button.pack(pady=10)

        # Zone de texte pour afficher les résultats
        self.result_textbox = ctk.CTkTextbox(self, width=760, height=400, wrap="none")
        self.result_textbox.pack(pady=10)

    def execute_query(self):
        query_index = int(self.query_var.get().split('.')[0])
        queries = [
            "SELECT nom_produit, prix_unitaire FROM produit;",
            "SELECT COUNT(id_client) AS nombre_de_clients FROM clients;",
            "SELECT AVG(prix_unitaire) AS moyenne_prix FROM produit;",
            "SELECT AVG(salaire) AS moyenne_salaire FROM commercents;",
            "SELECT nom, prenom, date_dernier_achat FROM clients ORDER BY date_dernier_achat DESC;",
            "SELECT p.nom_produit, COUNT(v.id_produit) AS nombre_ventes FROM ventes AS v INNER JOIN produit AS p ON p.id_produit=v.id_produit GROUP BY p.nom_produit ORDER BY nombre_ventes DESC LIMIT 10;",
            "SELECT c.nom, c.prenom, COUNT(v.id_produit) AS nombre_achats FROM ventes AS v INNER JOIN clients AS c ON c.id_client=v.id_client GROUP BY c.nom, c.prenom ORDER BY nombre_achats DESC;",
            "SELECT co.nom, co.prenom, COUNT(v.id_vente) AS nombre_ventes FROM ventes AS v INNER JOIN commercents AS co ON co.id_commercent=v.id_commercent GROUP BY co.nom, co.prenom ORDER BY nombre_ventes DESC;",
            "SELECT co.nom, co.prenom, p.nom_produit, COUNT(p.id_produit) AS nombre_ventes FROM commercents AS co INNER JOIN ventes AS v ON co.id_commercent=v.id_commercent INNER JOIN produit AS p ON p.id_produit=v.id_produit GROUP BY co.nom, co.prenom, p.nom_produit ORDER BY nombre_ventes DESC;",
            "SELECT c.nom, c.prenom, p.nom_produit, COUNT(p.id_produit) AS nombre_achat_duproduit FROM clients AS c INNER JOIN ventes AS v ON c.id_client=v.id_client INNER JOIN produit AS p ON p.id_produit=v.id_produit GROUP BY c.nom, c.prenom, p.nom_produit ORDER BY nombre_achat_duproduit DESC;",
            "SELECT co.id_commercent, co.nom, co.prenom, SUM(v.prix_unitaire * v.quantite) AS total_ventes FROM commercents co JOIN ventes v ON co.id_commercent = v.id_commercent GROUP BY co.id_commercent, co.nom, co.prenom;",
            "SELECT co.id_commercent, co.nom, co.prenom, SUM(v.quantite) AS total_vendu FROM commercents co JOIN ventes v ON co.id_commercent = v.id_commercent GROUP BY co.id_commercent, co.nom, co.prenom HAVING total_vendu > 10;",
            "UPDATE commercents SET salaire = salaire + 500 WHERE id_commercent IN (SELECT v.id_commercent FROM ventes v GROUP BY v.id_commercent HAVING SUM(v.quantite) > 10);",
            "UPDATE clients SET remise = 0.10 WHERE id_client IN (SELECT v.id_client FROM ventes v GROUP BY v.id_client HAVING COUNT(v.id_vente) > 5);",
            "SELECT p.nom_produit, COUNT(v.id_vente) AS nombre_ventes FROM produit p JOIN ventes v ON p.id_produit = v.id_produit GROUP BY p.id_produit ORDER BY nombre_ventes DESC;"
        ]

        query = queries[query_index - 1]
        try:
            if query.lower().startswith("select"):
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                self.result_textbox.delete("1.0", tk.END)
                self.result_textbox.insert("1.0", f"{columns}\n")
                for row in result:
                    self.result_textbox.insert(tk.END, f"{row}\n")
            else:
                cursor.execute(query)
                conn.commit()
                self.result_textbox.delete("1.0", tk.END)
                self.result_textbox.insert("1.0", "Requête exécutée avec succès.")
        except Exception as e:
            self.result_textbox.delete("1.0", tk.END)
            self.result_textbox.insert("1.0", f"Erreur: {str(e)}")

if __name__ == "__main__":
    app = SQLQueryApp()
    app.mainloop()

# Fermer la connexion à la base de données lorsque l'application est terminée
conn.close()
