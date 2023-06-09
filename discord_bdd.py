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


    def getUserID(self, mail):
        self.cursor.execute("SELECT id_utilisateur FROM Utilisateurs WHERE email_utilisateur = %s", (mail,))
        id = self.cursor.fetchone()
        return id


    def get_messages(self, id_channel):
        query = "SELECT * FROM messages WHERE id_channel = %s ORDER BY date_envoi DESC, heure_envoi DESC"
        self.cursor.execute(query, (id_channel,))
        messages = self.cursor.fetchall()
        return messages
    
    def get_channelID(self, usernameA, usernameB):
        query = "SELECT id_channel FROM canaux WHERE id_utilisateur1 = %s AND id_utilisateur2 = %s"
        self.cursor.execute(query, (usernameA, usernameB))
        id = self.cursor.fetchone()
        return id


    def create_message(self, text,date,hour,id_user, id_channel):
        self.cursor.execute("INSERT INTO Messages (text,date_envoi,heure_envoi, id_utilisateur, id_channel) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (text, date, hour,id_user, id_channel))
        self.connection.commit()
        test = "message send"
        return test


    def create_user(self, f_name, name, email, mdp):
        self.cursor.execute("INSERT INTO Utilisateurs (nom, prenom, email_utilisateur, mot_de_passe) VALUES (%s, %s, %s, %s)"
                            , (f_name,name,email, mdp))
        self.connection.commit()
        print(self.connection.commit())


    def create_channel(self, userA, userB):
        self.cursor.execute("INSERT INTO Canaux (id_utilisateur1, id_utilisateur2) VALUES (%s, %s)", (userA, userB))
        self.connection.commit()


# a modifier pour que cette fonction ne retourne que les canaux d'un id en particulier
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
