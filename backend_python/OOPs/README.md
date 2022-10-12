# Main points related to OOP

I will try to explain the implementation of OOPs in Python as simply as possible.

**Classes, Attributes, Methods:**
 
- To create a ***class***, we need to write:
```python
class OurClass:
```

- To create a ***attributes*** for our class, we need to write:
```python
class OurClass:
  first_attributes = "Hello World!"

print(OurClass.first_attributes) # call the attributes
```

***Method & Instance*** 

To create a ***method & instance*** for our class, we need to write self- required parameter:
```python
class OurClass:
  def method_hello(self):
    print('Hello World!')
    
our_first_instance = OurClass() # create an instance of the class
our_first_instance.method_hello() # call the method, returned Hello World!
```

***Initializer*** 

__init__: self = lionel_messi (instance of the class) 
```python
class FootballPlayer:
    def __init__(self, name, club, position, age):
        self.name = name
        self.club = club
        self.position = position
        self.age = age

lionel_messi = FootballPlayer('Lionel Messi', 'PSG', 'Right Winger', 35)
print(lionel_messi.position) # call the position, returned: Right Winger
```

***@staticmethod*** 

Allows you to call class parameters without declaring an instance. In simple terms - makes a normal function
```python
class OurClass:
    @staticmethod
    def method_hello():
        print('Hello World!')

OurClass.method_hello() # returned: Hello World!
# the same
our_first_instance = OurClass() 
our_first_instance.method_hello() # call the method, returned Hello World!
```

***Encapsulation:***

Allows you to hide the behavior of an object inside a class through __something
```python
class FootballPlayer:
    def name_messi(self):
        print('He is Lionel')
    __name = 'Lionel'
    
    def __age_messi(self):
        print('He is 35 years old!')
    age = 35

lionel_messi = FootballPlayer()
lionel_messi.name_messi() # method, retruned: He is Lionel
print(lionel_messi.__name()) # PRIVATE ATTRIBUTE, returned: Error   !!!!!!!!!!!!
lionel_messi.__age_messi() # PRIVATE METHOD, returned: Error   !!!!!!!!!!!!
print(lionel_messi.age) # attr, returned: 35
```
