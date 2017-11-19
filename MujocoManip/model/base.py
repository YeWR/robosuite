import os
import xml.etree.ElementTree as ET
import numpy as np
from mujoco_py import load_model_from_path
from MujocoManip.miscellaneous import XMLError
import xml.dom.minidom

class MujocoXML(object):
    """
        Base class of Mujoco xml file
        Wraps around ElementTree and provides additional functionality for merging different models.
        Specially, we keep track of <worldbody/>, <actuator/> and <asset/>
    """
    def __init__(self, fname):
        """
            Loads a mujoco xml from file specified by fname
        """
        self.file = fname
        self.folder = os.path.dirname(fname)
        self.tree = ET.parse(fname)
        self.root = self.tree.getroot()
        self.name = self.root.get('model')
        self.worldbody = self.create_default_element('worldbody')
        self.actuator = self.create_default_element('actuator')
        self.asset = self.create_default_element('asset')
        self.resolve_asset_dependency()

    def resolve_asset_dependency(self):
        """
            Convert every file dependency into absolute path so when we merge we don't break things.
        """
        for node in self.asset.findall('./*[@file]'):
            file = node.get('file')
            abs_path = os.path.abspath(self.folder)
            abs_path = os.path.join(abs_path, file)
            node.set('file', abs_path)


    def create_default_element(self, name):
        """
            Create a <@name/> tag under root if there is none
        """
        found = self.root.find(name)
        if found is not None:
            return found
        ele = ET.Element(name)
        self.root.append(ele)
        return ele


    def merge(self, other):
        """
            Default merge method
            @other is another MujocoXML instance
            raises XML error if @other is not a MujocoXML instance
            merges <worldbody/>, <actuator/> and <asset/> of @other into @self 
        """
        if not isinstance(other, MujocoXML):
            raise XMLError('{} is not a MujocoXML instance.'.format(type(other)))
        for body in other.worldbody:
            self.worldbody.append(body)
        for one_asset in other.asset:
            self.asset.append(one_asset)
        for one_actuator in other.actuator:
            self.actuator.append(one_actuator)
        # self.config.append(other.config)

    def get_model(self):
        """
            Returns a MJModel instance from the current xml tree
        """
        tempfile = os.path.join(self.folder, '.mujocomanip_temp_model.xml')
        with open(tempfile, 'w') as f:
            f.write(ET.tostring(self.root, encoding='unicode'))
        model = load_model_from_path(tempfile)
        os.remove(tempfile)
        return model

    def save_model(self, fname, pretty=False):
        """
            Saves the xml to file
            params:
            @fname output file location
            @pretty Attempts!! to pretty print the output
        """
        with open(fname, 'w') as f:
            xml_str = ET.tostring(self.root, encoding='unicode')
            if pretty:
                # TODO: get a good pretty print library
                parsed_xml = xml.dom.minidom.parseString(xml_str)
                xml_str = parsed_xml.toprettyxml(newl='')
            f.write(xml_str)
