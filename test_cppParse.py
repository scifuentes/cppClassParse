import unittest
import cppParse as sut

class TextToBlocksTest(unittest.TestCase):
    def test_classScope(self):
        text='''
class Foo : public Bar<T::C>
{
blabla;
blabla;
}
'''
        scopes = sut.textToScopes(text)
        
        self.assertEqual(len(scopes),1)
        s0=scopes[0]
        self.assertEqual(s0.key,'class')
        self.assertEqual(s0.name,'Foo : public Bar<T::C>')

    def test_classInNamespace(self):
        text='''
namespace Pez{
class Foo : public Bar<T::C>
{
blabla;
blabla;
};
}
'''
        scopes = sut.textToScopes(text)
        
        self.assertEqual(len(scopes),2)
        s0,s1=scopes
        self.assertEqual(s0.key,'namespace')
        self.assertEqual(s0.name,'Pez')
        self.assertEqual(len(s0.childs),1)
        self.assertEqual(s0.childs[0],s1)

        self.assertEqual(s1.parent,s0)
        self.assertEqual(s1.key,'class')
        self.assertEqual(s1.name,'Foo : public Bar<T::C>')

    def test_classWithMethods(self):
        text='''
class Foo : public Bar<T::C>
{
    double a;
    void foo(){}
    void bar(){ if(paf){zas;}}
};
'''
        scopes = sut.textToScopes(text)

        self.assertEqual(len([scope for scope in scopes if scope.key == 'class']),1)
        s0=scopes[0]
        self.assertEqual(s0.key,'class')
        self.assertEqual(s0.name,'Foo : public Bar<T::C>')
        self.assertEqual(len(s0.childs),2)

    def test_otherScopes(self):
        text='''
class Foo : public Bar<T::P> 
{  
    double a;  
    void foo()
    { int blabla;  
      bar(); 
      if(blabla){popo;} 
      for(i =0;;){puf();}
    } 
};
'''
        scopes = sut.textToScopes(text)

        self.assertEqual(len(scopes),4)
        self.assertEqual(scopes[0].key,'class')
        self.assertEqual(scopes[1].key,'foo')
        self.assertEqual(scopes[2].key,'if')
        self.assertEqual(scopes[3].key,'for')



if __name__ == '__main__':
    unittest.main(verbosity=2)