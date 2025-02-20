import pickle

# Authentication logic (this is a placeholder for demo purposes)
def authenticate_user(username, password):
    try:
        with open("users.pkl", "rb") as f:
            users = pickle.load(f)
        
        if username in users and users[username] == password:
            return True
        return False
    except FileNotFoundError:
        return False

# Create new user logic
def create_user(username, password):
    try:
        # Load existing users or create a new dictionary
        users = {}
        try:
            with open("users.pkl", "rb") as f:
                users = pickle.load(f)
        except FileNotFoundError:
            pass
        
        # Add the new user
        users[username] = password
        
        # Save updated users dictionary
        with open("users.pkl", "wb") as f:
            pickle.dump(users, f)
    except Exception as e:
        print(f"Error in creating user: {e}")