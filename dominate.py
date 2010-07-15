from xml.dom import minidom
from xml.dom import EMPTY_NAMESPACE
import re

ATOM_NS = 'http://www.w3.org/2005/Atom'
INPUTFILE = 'atom_data_in.xml'
OUTPUTFILE = 'atom_data_out.xml'

def get_text_from_construct(element):
    '''
    Return the content of an Atom element declared with the
    atomTextConstruct pattern.  Handle both plain text and XHTML
    forms.  Return a UTF-8 encoded string.
    '''
    if element.getAttributeNS(EMPTY_NAMESPACE, u'type') == u'xhtml':
        # grab the XML serialization of each child
        childtext = [ c.toxml('utf-8') for c in element.childNodes ]
        # and stitch it together
        content = ''.join(childtext).strip()
        return content
    else:
        return element.firstChild.data.encode('utf-8')

if __name__ == "__main__":

    # config
    atom_out = open(OUTPUTFILE, 'w')
    re_title = re.compile('class="title">(.*?)<\/td>', re.U | re.M | re.S)
    re_table = re.compile('^<table.*?<\/table>[\w\n]*', re.U | re.M | re.S)

    # dump first 2 lines of metadata to the output file
    with open(INPUTFILE, 'r') as f:
        result = re.match('(.*)<entry>', f.readline(), re.U | re.M)
        if result:
            atom_out.write(result.group(1))

    # now we read it all XML DOM-like
    atom_in = minidom.parse(INPUTFILE)
    atom_in.normalize()

    feedtitle_element = atom_in.getElementsByTagNameNS(ATOM_NS, u'title')[0]
    print 'Processing ATOM 1.0 feed: ', get_text_from_construct(feedtitle_element)

    entries = []
    for entry in atom_in.getElementsByTagNameNS(ATOM_NS, u'entry'):
        title_element = entry.getElementsByTagNameNS(ATOM_NS, u'title')[0]
        # we're only interested in the posts, which (oddly) have no title
        if title_element.firstChild == None:
            print "\nFound a post! Processing..."
            content_element = entry.getElementsByTagNameNS(ATOM_NS, u'content')[0]
            content = get_text_from_construct(content_element)
            print "OLD CONTENT: " + content[:65]

            # regex to get title, replace title element in entry
            title_match = re_title.search(content)
            if title_match:
                new_title = unicode(title_match.group(1))
            else:
                new_title = u'*** NO TITLE! ***'
            title_node = atom_in.createTextNode(new_title)
            title_element.appendChild(title_node)
            print "TITLE: " + get_text_from_construct(title_element)

            # regex to get rid of table, replace content element in entry
            #new_content = re_table.sub("", content, count=1)
            (new_content, count) = re_table.subn("", content, count=1)
            if count == 0:
                print "*** sub() failed to match!"
            content_element.firstChild.data = new_content
            print "NEW CONTENT: " + get_text_from_construct(content_element)[:65]

            # remove 3 link elements (?)
            links = entry.getElementsByTagNameNS(ATOM_NS, u'link')
            for link in links:
                entry.removeChild(link)
                link.unlink() # pun!
            
            # cleanup author element (?)
            author = entry.getElementsByTagNameNS(ATOM_NS, u'author')[0]
            for node in author.childNodes:
                if getattr(node, 'tagName', None) in [u'uri', u'email']:
                    author.removeChild(node)
                    node.unlink()
                #else:
                #    if getattr(node, 'data', None) == u'\n      ':
                #        author.removeChild(node)
                #        node.unlink()
            
            # TODO: append entry to list
            entries.append(entry)
            
        else:
            print "(Skipping '" + get_text_from_construct(title_element) + "')"

    # reverse the list of entries & write them to output file
    entries.reverse()
    for e in entries:
        atom_out.write(e.toxml())
    atom_out.write(u'\n</feed>\n')
    atom_out.close()
