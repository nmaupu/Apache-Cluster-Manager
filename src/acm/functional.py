## Package acm.funcitonal
class curry(object):
  '''Class to currify a function'''
  def __init__(*args, **kw):
    self = args[0]
    self.fn, self.args, self.kw = (args[1], args[2:], kw)

  def __call__(self, *args, **kw):
    if kw and self.kw:
      d = self.kw.copy()
      d.update(kw)
    else:
      d = kw or self.kw
    return self.fn(*(self.args + args), **d)
