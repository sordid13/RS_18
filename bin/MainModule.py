from bin import *
import pickle
import os


class MainModule:
    def __init__(self, evManager):
        globals()
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        if not os.path.exists("../users"):
            os.makedirs("../users")

        self.folder = ""

    def LoadAssets(self):
        # Load list of ingredients
        config = configparser.ConfigParser()
        config.read("data/ingredients.rs")
        for section in config.sections():
            name = str(config.get(section, "name"))
            type = str(config.get(section, "type"))
            baseCost = config.getfloat(section, "cost")
            INGREDIENTS_LIST.append(Ingredient(name, type, baseCost))

        # Load list of dishes
        config = configparser.ConfigParser()  # Reinitiate for new file
        config.read("data/dishes.rs")
        for section in config.sections():
            name = str(config.get(section, "name"))
            type = str(config.get(section, "type"))
            cuisine = str(config.get(section, "cuisine"))
            rawIngre = str(config.get(section, "ingredients")).strip()

            ingredients = []
            split = rawIngre.split(', ')
            for ingredient in split:
                noIngredient = True
                for i in INGREDIENTS_LIST:
                    if ingredient == i.name:
                        ingredients.append(i)
                        noIngredient = False
                        break
                if noIngredient:
                    print(ingredient)

            dish = Dish(name, type, cuisine, ingredients)
            DISHES_LIST.append(dish)
            if cuisine == "Western":
                WESTERN_DISHES.append(dish)
            elif cuisine == "Chinese":
                CHINESE_DISHES.append(dish)
            elif cuisine == "Korean":
                KOREAN_DISHES.append(dish)

        print(len(INGREDIENTS_LIST))

    def NewGame(self):
        saves = [x[0] for x in os.walk(self.folder)] # Return child directories ... first entry is self.folder
        newSave = self.folder + "/save" + str(len(saves))
        os.makedirs(newSave)

        return newSave

    def StartGame(self, new=None, save=None):
        if new:
            folder = self.NewGame()
            with Game(folder, self.evManager) as game:
                import dill
                with open(folder + "/game.save", "wb") as file:
                    dill.dump(game, file)

        elif save:
            with open(self.folder+"/"+save+"/game.save", "rb") as file:
                import pickle
                game = pickle.load(file)
                game.evManager = self.evManager
                self.evManager.RegisterListener(game)
                ev = GameStartedEvent(game.players)
                self.evManager.Post(ev)
                print("yes")

    def Start(self):
        view = View(self.evManager)
        control = Controller(self.evManager)
        control.Run()

    def Notify(self, event):
        if isinstance(event, AuthenticatedEvent):
            self.folder = "../users/" + event.user
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

            self.LoadAssets()
            self.Start()

        elif isinstance(event, NewGameRequestEvent):
            self.StartGame(new=True)

        elif isinstance(event, SaveGameRequestEvent):
            self.StartGame(save="save1")
            #self.SaveGame()


def main():
    Main.evManager = EventManager()
    print(Main.evManager)
    auth = Authentication(Main.evManager)
    mainModule = MainModule(Main.evManager)

    auth.mainloop()

if __name__ == "__main__":
    main()

