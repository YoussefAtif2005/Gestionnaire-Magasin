--Creation des tables nécessaires--
CREATE TABLE produit(
id_produit int PRIMARY KEY NOT NULL,
nom_produit text NOT NULL,
pays text NOT NULL,
quantite text NOT NULL,
prix_unitaire float NOT NULL,
categorie VARCHAR(30)
);
ALTER TABLE ventes DROP COLUMN id_produit
ALTER TABLE ventes ADD COLUMN id_produit INT REFERENCES produit(id_produit) 
CREATE TABLE clients(
id_client int PRIMARY KEY NOT NULL,
nom text NOT NULL,
prenom text NOT NULL,
date_naissance date NOT NULL,
sexe text NOT NULL,
numero_tel int NOT NULL, 
date_dernier_achat date NOT NULL
);

CREATE TABLE commercents(
id_commercent int PRIMARY KEY NOT NULL,
nom text NOT NULL,
prenom text NOT NULL,
salaire float NOT NULL,
date_embauche date NOT NULL,
num_tel text NOT NULL
);

CREATE TABLE ventes(
id_vente int PRIMARY KEY NOT NULL,
id_client int NOT NULL,
id_commercent int NOT NULL,
id_produit int NOT NULL,
quantite int NOT NULL,
prix_unitaire float NOT NULL,
FOREIGN KEY (id_client) REFERENCES clients(id_client),
FOREIGN KEY (id_commercent) REFERENCES commercents(id_commercent),
FOREIGN KEY (id_produit) REFERENCES produit(id_produit)
);

---Les requettes--

--1.Le nom et le prix de tous les produits--

SELECT nom_produit, prix_unitaire
FROM produit;

--2.Le nombre de clients

SELECT COUNT(id_client) AS nombre_de_clients
FROM clients;

--3. La moyenne des prix dans des produits

SELECT ROUND(AVG(prix_unitaire), 2) AS prix_moyen
FROM produit;

--4. La moyenne des salaires des commercents

SELECT ROUND(AVG(salaire), 2) AS moyenne_salaire
FROM commercents;

--5. Les clients ayant fait des achats récemment

SELECT nom, prenom, date_dernier_achat FROM clients
ORDER BY date_dernier_achat DESC;


--6.Le nom des 10 produits les plus vendus

SELECT p.nom_produit, COUNT(v.id_produit) AS nombre_ventes
FROM ventes AS v
INNER JOIN produit AS p
ON p.id_produit=v.id_produit
GROUP BY p.nom_produit
ORDER BY COUNT(v.id_produit) DESC
LIMIT 10;

--7.Le nom des clients les plus fidèles 

SELECT c.nom, c.prenom, COUNT(v.id_produit) AS nombre_achats
FROM ventes AS v
INNER JOIN clients AS c
ON c.id_client=v.id_client
GROUP BY c.nom, c.prenom
ORDER BY COUNT(v.id_produit) DESC;

--8.Le classement des commercents selon le nombre des ventes qu'ils ont effectuées
SELECT co.nom, co.prenom, COUNT(v.id_vente) AS nombre_ventes
FROM ventes AS v
INNER JOIN commercents AS co
ON co.id_commercent=v.id_commercent
GROUP BY co.nom, co.prenom
ORDER BY COUNT(v.id_vente) DESC;

--9. Calculer le chiffre d'affaire généré par commercent

SELECT co.id_commercent, co.nom, co.prenom, SUM(v.prix_total) AS total_ventes
FROM commercents co
JOIN ventes v ON co.id_commercent = v.id_commercent
GROUP BY co.id_commercent, co.nom, co.prenom;

--10. Afficher les commercents ayant vendu plus de 10 produits

SELECT co.id_commercent, co.nom, co.prenom, SUM(v.quantite) AS total_vendu
FROM commercents co
JOIN ventes v ON co.id_commercent = v.id_commercent
GROUP BY co.id_commercent, co.nom, co.prenom
HAVING SUM(v.quantite) > 10;

--11. Mettre à jour le salaire des commercents ayant vendu plus de 10 produits en ajoutant une prime

UPDATE commercents co
SET salaire = salaire + 500  -- La prime de 500 est ajoutée
WHERE (SELECT SUM(v.quantite)
       FROM ventes v
       WHERE v.id_commercent = co.id_commercent) > 5;
	   
--12. Mettre à jour les clients ayant effectué plus de 5 achats pour leur appliquer une remise de 10%

UPDATE clients c
SET remise = 0.10
WHERE (SELECT COUNT(v.id_vente)
       FROM ventes v
       WHERE v.id_client = c.id_client) > 2;	

--13 Obtenez le nombre de ventes pour chaque produit

SELECT p.nom_produit,COUNT(v.id_vente) AS number_of_sales
FROM produit p
JOIN ventes v ON p.id_produit = v.id_produit
GROUP BY p.id_produit, p.nom_produit
ORDER BY number_of_sales DESC;

--14.nombre total des produits par categorie
SELECT categorie, SUM(quantite) AS total_produits
FROM produit
GROUP BY categorie;


--15nombre total des produits vendus par categorie
SELECT p.categorie, SUM(v.quantite) AS total_quantity_sold
FROM produit p
JOIN ventes v ON p.id_produit = v.id_produit
GROUP BY p.categorie;


--16.le chiffre d'affaire de chaque categorie de produit
SELECT p.categorie, SUM(v.quantite * v.prix_unitaire) AS chiffre_affaire
FROM produit p
JOIN ventes v ON p.id_produit = v.id_produit
GROUP BY p.categorie;



