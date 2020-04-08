class BlogObject(object):

    def __init__(self, id, title, description, content, image, date, pin):
        self.id = id
        self.image = image
        self.title = title
        self.description = description
        self.content = content
        self.date = date
        self.pin = pin
