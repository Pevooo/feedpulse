class Spark():
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Spark, cls).__new__(cls)
    return cls.instance
  
  def add(self):
    pass
  
  def delete(self):
    pass
  
  def  query(self):
    pass
  
  def modify(self):
    pass


spark_instance = Spark()