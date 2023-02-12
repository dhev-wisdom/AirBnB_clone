#!/usr/bin/python3
"""
A module that contains our hbnb console
"""


import re
import cmd
import subprocess
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    The HBNB console class
    """

    prompt = "(hbnb) "

    all_models = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "State": State, "City": City, "Amenity": Amenity,
                  "Review": Review}

    user_commands = ["all", "count"]

    def do_quit(self, line):
        """ Simple command to exit the console """
        return True

    def do_EOF(self, line):
        """ EOF exits the console """
        return True

    def do_shell(self, line):
        """ Used to run default shell command """
        try:
            result = subprocess.run(line, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=True,
                                    check=True)
            print(result.stdout.decode().strip())
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode().strip())

    def do_create(self, line):
        """ Creates a new instance of BaseModel """
        if len(line) == 0:
            print("** class name missing **")
        elif line not in HBNBCommand.all_models:
            print("** class doesn't exist **")
        else:
            new_model = HBNBCommand.all_models[line]()
            new_model.save()
            print(new_model.id)

    def do_show(self, line):
        """
        Prints the string representation of an
        instance based on the class name and id
        """
        all_classes = models.storage.all()
        if len(line) == 0:
            print("** class name missing **")
        else:
            _line = line.split()
            name = _line[0]
            _id = None
            if len(_line) > 1:
                _id = _line[1]
            if name not in HBNBCommand.all_models:
                print("** class doesn't exist ** ")
            elif _id is None:
                print("** instance id missing **")
            elif name + "." + _id not in all_classes:
                print("** no instance found **")
            else:
                print(all_classes[name + "." + _id].__str__())

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file)
        """

        all_classes = models.storage.all()
        if len(line) == 0:
            print("** class name missing **")
        else:
            _line = line.split()
            name = _line[0]
            _id = None
            if len(_line) > 1:
                _id = _line[1]
            if name not in HBNBCommand.all_models:
                print("** class doesn't exist **")
            elif _id is None:
                print("** instance id missing **")
            elif name + "." + _id not in all_classes:
                print("** no instance found **")
            else:
                all_objects = models.storage.all()
                del all_objects[name + "." + _id]
                models.storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all
        """

        all_objects = models.storage.all()
        if len(line) > 0 and line in HBNBCommand.all_models:
            print([v.__str__() for k, v in
                  all_objects.items() if
                  v.__class__.__name__ == line])
        elif len(line) > 0 and line not in HBNBCommand.all_models:
            print("** class doesn't exist ** ")
        else:
            print([v.__str__() for k, v in all_objects.items()])

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)
        """

        _line = line.split()
        all_classes = models.storage.all()
        if len(line) == 0:
            print("** class name missing **")
        else:
            name = _line[0]
            _id = None
            if len(_line) > 1:
                _id = _line[1]
            if name not in HBNBCommand.all_models:
                print("** class doesn't exist ** ")
            elif _id is None:
                print("** instance id missing **")
            elif name + "." + _id not in all_classes:
                print("** no instance found **")
            elif len(_line) < 3:
                print("** attribute name missing **")
            elif len(_line) < 4:
                print("** value missing **")
            elif (_line[2] == "id" or _line[2] == "created_at"
                  or _line[2] == "updated_at"):
                print("Illegal update")
                pass
            else:
                val = None
                if _line[3].isnumeric():
                    val = eval(_line[3])
                elif _line[3][0] == "\"" or _line[3][0] == "\'":
                    val = eval(_line[3])
                else:
                    val = _line[3]
                setattr(all_classes[name + "." + _id], _line[2], val)
                models.storage.save()

    def default(self, line):
        """ Handles default command entered by the user """
        cls_name = ("".join(re.findall("^[A-Z]{1}[A-Za-z]+[.]", line)))
        comd = ("".join(re.findall("[.]{1}[a-z]+[(]", line)))
        arg = ("".join(re.findall("[(]{1}.*[)]", line)))
        if len(cls_name) == 0 or len(comd) == 0 or len(arg) == 0:
            print("Invalid Command")
            return False
        else:
            cls_name, comd, arg = cls_name[:-1], comd[1:-1], arg[1:-1]
        if cls_name not in self.all_models:
            print("class not found")
            return False
        elif comd not in self.user_commands:
            print("command not found")
            return False
        # Function calls
        if len(arg) == 0:
            # handle call without args
            eval("self." + comd + "('" + cls_name + "')")
        else:
            # handle calls with args
            eval("self." + comd + "('" + cls_name + "', '" + arg + "')")

    def all(self, cls_name):
        """ Returns all the instance of a Model """
        self.do_all(cls_name)

    def count(self, cls_name):
        """ Count the number of instances of a model """

        all_objects = models.storage.all()
        if cls_name in HBNBCommand.all_models:
            all_inst = ([v.__str__() for k, v in
                        all_objects.items() if
                        v.__class__.__name__ == cls_name])
            print(len(all_inst))
        else:
            print(0)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
