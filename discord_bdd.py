import mysql.connector

class Discord_bdd:

    def __init__(self, user, password, database, host='localhost'):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def get_messages(self, id_canal):
        query = "SELECT * FROM messages WHERE id_canal = %s ORDER BY date_envoi DESC, heure_envoi DESC"
        self.cursor.execute(query, (id_canal,))
        messages = self.cursor.fetchall()
        return messages

    def create_message(self, text,date,hour,id_user, id_canal):
        self.cursor.execute("INSERT INTO Messages (text,date_envoi,heure_envoi, id_utilisateur, id_canal) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (text, date, hour,id_user, id_canal))
        self.connection.commit()

    def update_message(self, text, id_utilisateur, id_canal):
        self.cursor.execute("UPDATE Messages SET message = %s WHERE id = %s", (text, id_utilisateur, id_canal))
        self.connection.commit()

    def delete_message(self, id):
        self.cursor.execute("DELETE FROM Messages WHERE id = %s", (id,))
        self.connection.commit()

    def create_user(self, f_name, name, email, mdp):
        self.cursor.execute("INSERT INTO Utilisateurs (nom, prenom, email_utilisateur, mot_de_passe) VALUES (%s, %s, %s, %s)"
                            , (f_name,name,email, mdp))
        self.connection.commit()
        print(self.connection.commit())

    def get_user(self, nom):
        self.cursor.execute("SELECT * FROM Utilisateurs WHERE nom = %s", (nom,))
        return self.cursor.fetchone()

    def create_discussion(self, nom):
        self.cursor.execute("INSERT INTO Discussions (nom_discussion) VALUES (%s)", (nom,))
        self.connection.commit()

    def get_discussion(self, nom):
        self.cursor.execute("SELECT * FROM Discussions WHERE nom_discussion = %s", (nom,))
        return self.cursor.fetchone()

    def get_all_discussions(self):
        self.cursor.execute("SELECT * FROM Discussions")
        return self.cursor.fetchall()

    def create_canal(self, nom,description, canal):
        self.cursor.execute("INSERT INTO Canaux (nom_canal, description, type_canal) VALUES (%s, %s, %S)", (nom, description, canal))
        self.connection.commit()

    def get_canal(self, nom):
        self.cursor.execute("SELECT * FROM Canaux WHERE nom_canal = %s", (nom,))
        return self.cursor.fetchone()

    def get_all_canaux(self):
        self.cursor.execute("SELECT * FROM Canaux")
        return self.cursor.fetchall()

    def check_login(self, username, password):
        self.cursor.execute("SELECT * FROM Utilisateurs WHERE email_utilisateur = %s AND mot_de_passe = %s", (username, password))
        return self.cursor.fetchone()
    def sign_in(self, f_name,name, password, mail):
        self.cursor.execute("SELECT * FROM Utilisateurs WHERE nom_utilisateur = %s", (name,))
        if self.cursor.fetchone() is None:
            self.create_user(f_name,name, password, mail)
            return True
        else:
            return False
