import unittest
import classDiag as sut

##@unittest.skip
class ClassMatchingTest(unittest.TestCase):
    def test_NoParent(self):
        fileText='class Foo\n{   blabla\n};'
        classes = sut.getClassDefinitions(fileText)
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].name, 'Foo')
        self.assertEqual(classes[0].parents, '')

    def test_SimpleParent(self):
        fileText = 'class Foo : public Bar\n{\n   blabla\n};'
        classes = sut.getClassDefinitions(fileText)
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].name, 'Foo')
        self.assertEqual(classes[0].parents, 'public Bar')

    def test_FunnyParent(self):
        fileText = 'class Foo : public Bar\n, std::iterator<std::forward_iterator_tag,\n boost::shared_ptr<std::string> >::Bar<Zoo::Paz>\n{\n   blabla\n};'
        classes = sut.getClassDefinitions(fileText)
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0].name, 'Foo')
        self.assertEqual(classes[0].parents, 'public Bar, std::iterator<std::forward_iterator_tag, boost::shared_ptr<std::string> >::Bar<Zoo::Paz>')

class ParentExtractionTest(unittest.TestCase):
    def test_SimpleOne(self):
        parentsLine = 'public Foo'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 1)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')

    def test_TwoSimpleParents(self):
        parentsLine = 'public Foo, private Bar'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Bar')
        
    def test_NoPrivacyOne(self):
        parentsLine = 'Foo'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 1)
        self.assertEqual(parents[0].privacy, 'private')
        self.assertEqual(parents[0].simpleType, 'Foo')
        
    def test_NoPrivacyTwo(self):
        parentsLine = 'public Foo, Bar'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Bar')
        
    def test_TemplatedParent(self):
        parentsLine = 'public Foo, private Bar<Zoo>'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Bar')
        
    def test_MultyTemplatedParent(self):
        parentsLine = 'public Foo, private Bar<Zoo, Paz>'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Bar')

    def test_NamespaceParent(self):
        parentsLine = 'public Foo, private Bar::Zoo'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Zoo')

    def test_FunnyOne(self):
        parentsLine = 'public Foo, std::iterator<std::forward_iterator_tag, boost::shared_ptr<std::string> >::Bar'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Bar')
        self.assertEqual(parents[1].qualifiedType, 'std::iterator<std::forward_iterator_tag, boost::shared_ptr<std::string> >::Bar')

    def test_FunnyTwo(self):
        parentsLine = 'public Foo, std::iterator<std::forward_iterator_tag, boost::shared_ptr<std::string> >::Bar<Zoo::Paz>'
        parents = sut.extractParents(parentsLine)
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[0].privacy, 'public')
        self.assertEqual(parents[0].simpleType, 'Foo')
        self.assertEqual(parents[1].privacy, 'private')
        self.assertEqual(parents[1].simpleType, 'Bar')
        self.assertEqual(parents[1].qualifiedType, 'std::iterator<std::forward_iterator_tag, boost::shared_ptr<std::string> >::Bar<Zoo::Paz>')

if __name__ == '__main__':
    unittest.main(verbosity=2)