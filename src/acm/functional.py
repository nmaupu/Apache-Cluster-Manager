# Copyright 2011 Nicolas Maupu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
