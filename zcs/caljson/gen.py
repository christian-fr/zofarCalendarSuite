__version__ = '0.0.2'

import re
import string
import math
from pathlib import Path
import os



class Question_QML_generator:
    def __init__(self, question_type: str, varname_stem: str, index: int = 1, question_text: str = ''):
        self.question_type = question_type
        self.valid_question_types = ['matrixDouble', 'matrixMultipleChoice', 'matrixQuestionMixed',
                                     'matrixQuestionOpen', 'matrixQuestionSingleChoice', 'multipleChoice',
                                     'questionOpen', 'questionSingleChoice']

        assert self.question_type in self.valid_question_types

        self.question_text = question_text
        self.dict_of_question_types = {}
        self.create_dict_of_question_types()
        self.generated_qml_string = ''

        self.index = index

        self.list_of_answer_option_uids = []
        self.list_of_answer_option_labels = []
        self.list_of_answer_option_values = []
        self.list_of_missing_answer_option_labels = []
        self.list_of_missing_answer_option_values = []
        self.list_of_missing_answer_option_uids = []
        self.list_of_item_questions = []
        self.varname_stem = varname_stem
        self.list_of_varnames = []
        self.variable_declaration_string = ''

    def create_question_qml(self) -> None:
        if self.question_type == 'matrixQuestionSingleChoice':
            self.generate_matrix_question_single_choice()
        elif self.question_type == 'questionOpen':
            self.generate_question_open()
        elif self.question_type == 'matrixDouble':
            self.generate_matrix_double()
        elif self.question_type == 'matrixMultipleChoice':
            self.generate_matrix_multiple_choice()
        elif self.question_type == 'matrixQuestionMixed':
            self.generate_matrix_question_mixed()
        elif self.question_type == 'matrixQuestionOpen':
            self.generate_matrix_question_open()
        elif self.question_type == 'multipleChoice':
            self.generate_multiple_choice()
        elif self.question_type == 'questionSingleChoice':
            self.generate_question_single_choice()
        else:
            raise NotImplementedError('Question type "' + self.question_type + '" not yet implemented.')

    def create_dict_of_question_types(self):
        for i in range(0, len(self.valid_question_types)):
            self.dict_of_question_types[i] = self.valid_question_types[i]

    def generate_question_open(self):
        self.generated_qml_string = f"""\t\t\t<zofar:questionOpen uid="qo{self.index}" variable="{self.varname_stem}" size="4" type="text">\n"""
        self.generated_qml_string += """\t\t\t\t<zofar:header>\n"""
        if self.question_text.strip() != '':
            self.generated_qml_string += f"""\t\t\t\t\t<zofar:question uid="q1" block="true">{self.question_text}</zofar:question>\n"""
        self.generated_qml_string += """\t\t\t\t</zofar:header>\n"""
        self.generated_qml_string += """\t\t\t</zofar:questionOpen>\n\n"""

        if self.varname_stem not in self.list_of_varnames:
            self.list_of_varnames.append(self.varname_stem)
        self.variable_declaration_string += f'        <zofar:variable name="{self.varname_stem}" type="string"/>\n'

    def generate_matrix_double(self):
        raise NotImplementedError()

    def generate_matrix_multiple_choice(self):
        raise NotImplementedError()

    def generate_matrix_question_mixed(self):
        raise NotImplementedError()

    def generate_matrix_question_open(self):
        raise NotImplementedError()

    def generate_multiple_choice(self):
        raise NotImplementedError()

    def generate_question_single_choice(self):
        raise NotImplementedError

    def generate_matrix_question_single_choice(self):
        self.generated_qml_string = ''
        self.generated_qml_string += """\t\t\t<zofar:matrixQuestionSingleChoice uid="mqsc">\n\t\t\t\t<zofar:header>\n\t\t\t\t\t<zofar:question uid="q">\n"""
        self.generated_qml_string += '\t\t\t\t\t\t' + self.question_text + '\n'
        self.generated_qml_string += '''\t\t\t\t\t</zofar:question>\n\t\t\t\t</zofar:header>\n\t\t\t\t<zofar:responseDomain noResponseOptions="'''
        self.generated_qml_string += str(
            len(self.list_of_answer_option_labels) + len(self.list_of_missing_answer_option_labels))
        self.generated_qml_string += '''" uid="rd">\n\t\t\t\t\t<zofar:header>\n'''
        for i in range(0, len(self.list_of_answer_option_labels)):
            self.generated_qml_string += '\t\t\t\t\t\t<zofar:title uid="ti' + str(i + 1) + '">' + \
                                         self.list_of_answer_option_labels[i] + '</zofar:title>\n'
        self.generated_qml_string += '\t\t\t\t\t</zofar:header>\n\n'
        if len(self.list_of_missing_answer_option_labels) > 0:
            self.generated_qml_string += '\t\t\t\t\t<zofar:missingHeader>\n'
            for i in range(0, len(self.list_of_missing_answer_option_labels)):
                self.generated_qml_string += '\t\t\t\t\t\t<zofar:title uid="ti' + str(
                    i + 1 + len(self.list_of_answer_option_labels)) + '">' + \
                                             self.list_of_missing_answer_option_labels[i] + '</zofar:title>\n'
            self.generated_qml_string += '\t\t\t\t\t</zofar:missingHeader>\n\n'

        for i in range(0, len(self.list_of_item_questions)):
            self.generated_qml_string += '\t\t\t\t\t<zofar:item uid="it' + str(
                i + 1) + '">\n\t\t\t\t\t\t<zofar:header>\n\t\t\t\t\t\t\t<zofar:question uid="q">\n\t\t\t\t\t\t\t\t'
            self.generated_qml_string += self.list_of_item_questions[
                                             i] + '\n\t\t\t\t\t\t\t</zofar:question>\n\t\t\t\t\t\t</zofar:header>\n'
            self.generated_qml_string += '\t\t\t\t\t\t<zofar:responseDomain variable="'

            tmp_varname = self.varname_stem

            # assign letter suffixes to varname
            factor = math.floor(i / 26)
            if 1 <= factor <= 26:
                tmp_varname += string.ascii_lowercase[factor - 1]
            elif factor == 0:
                pass
            else:
                raise IndexError('Index out or range: ' + str(i) + ' - cannot assign a letter!')
            tmp_varname += string.ascii_lowercase[i % 26]

            self.generated_qml_string += tmp_varname
            if tmp_varname not in self.list_of_varnames:
                self.list_of_varnames.append(tmp_varname)

            self.generated_qml_string += '" uid="rd">\n'
            for j in range(0, len(self.list_of_answer_option_labels)):
                self.generated_qml_string += '\t\t\t\t\t\t\t<zofar:answerOption uid="ao' + str(
                    j + 1) + '" value="' + str(
                    self.list_of_answer_option_values[j]) + '" label="' + \
                                             self.list_of_answer_option_labels[j] + '"></zofar:answerOption>\n'

            for k in range(0, len(self.list_of_missing_answer_option_labels)):
                self.generated_qml_string += '\t\t\t\t\t\t\t<zofar:answerOption uid="ao' + str(
                    k + 1 + len(self.list_of_answer_option_labels)) + '" value="' + str(
                    self.list_of_missing_answer_option_values[k]) + '" label="' + \
                                             self.list_of_missing_answer_option_labels[
                                                 k] + '" missing="true"></zofar:answerOption>\n'

            self.generated_qml_string += '''\t\t\t\t\t\t</zofar:responseDomain>\n\t\t\t\t\t</zofar:item>\n\n'''

        self.generated_qml_string += '\t\t\t\t</zofar:responseDomain>\n\t\t\t</zofar:matrixQuestionSingleChoice>\n\n'

        for i in range(0, len(self.list_of_varnames)):
            self.variable_declaration_string += '<zofar:variable name="'
            self.variable_declaration_string += self.list_of_varnames[i]
            self.variable_declaration_string += '" type="singleChoiceAnswerOption"/>\n'

    def print_variable_declaration(self):
        print(self.variable_declaration_string)


class Question_QML_JSON_Trigger_generator:
    def __init__(self, number_of_fragment_variables: int = 10, fragment_variable_name_stem: str = 'episodes_fragment_'):
        self.list_of_question_qml_generator_objects = []
        self.json_function_code_load = ''
        self.json_function_code_save = ''

        self.number_of_fragment_variables = number_of_fragment_variables
        self.fragment_variable_name_stem = fragment_variable_name_stem
        self.list_of_fragment_variables_names = []

    @staticmethod
    def display_whole_json() -> str:
        tmp_display_whole_json = '<!-- display whole json -->'
        return tmp_display_whole_json

    def reset_whole_json(self) -> str:
        tmp_reset_whole_json_str = '			<!-- reset whole json -->\n'
        tmp_reset_whole_json_str += f"""			<zofar:action
				command="zofar.frac(zofar.list({','.join(self.list_of_fragment_variables_names)}),zofar.jsonArr2str(defrac))" onExit="true" direction="forward">
				<zofar:scriptItem value="zofar.assign('defrac',zofar.str2jsonArr(''))" />
			</zofar:action>\n\n"""
        return tmp_reset_whole_json_str

    def return_fragment_variable_qml_edit_code(self) -> str:
        tmp_list_of_open_question_qml_str = []
        for index, fragment_variable in enumerate(self.list_of_fragment_variables_names):
            tmp_question_object = Question_QML_generator(varname_stem=fragment_variable,
                                                         index=index + 1,
                                                         question_type='questionOpen',
                                                         question_text=f'{fragment_variable}: ')
            tmp_question_object.generate_question_open()
            tmp_list_of_open_question_qml_str.append(tmp_question_object.generated_qml_string)
        return '\n'.join(tmp_list_of_open_question_qml_str)

    def write_to_qml_file(self):
        # load template
        tmp_xml_str = Path(os.path.abspath(''), 'data', 'template', 'template_questionnaire.xml').read_text(encoding='utf-8')

        # create questionOpen for index page (setting of episode_index)
        tmp_question_open_episode_index_str = """
			<zofar:questionOpen uid="mqsc" variable="episode_index" size="4" type="text">
                <zofar:header>
                    <zofar:question uid="q1">episode_index</zofar:question>
                </zofar:header>
			</zofar:questionOpen>\n"""

        replacement_dict = {'variable_declaration': 'XXX_VARIABLE_DECLARATION_PLACEHOLDER_XXX',
                            'index_body': 'XXX_INDEX_BODY_PLACEHOLDER_XXX',
                            'index_trigger': 'XXX_INDEX_TRIGGERS_PLACEHOLDER_XXX',
                            'set_episode_index_body': 'XXX_SET_EPISODE_INDEX_BODY_PLACEHOLDER_XXX',
                            'set_episode_index_trigger': 'XXX_SET_EPISODE_INDEX_TRIGGERS_PLACEHOLDER_XXX',
                            'set_episode_data_body': 'XXX_SET_EPISODE_DATA_BODY_PLACEHOLDER_XXX',
                            'set_episode_data_trigger': 'XXX_SET_EPISODE_DATA_TRIGGERS_PLACEHOLDER_XXX',
                            'reset_json_array_body': 'XXX_RESET_JSON_ARRAY_BODY_PLACEHOLDER_XXX',
                            'reset_json_array_trigger': 'XXX_RESET_JSON_ARRAY_TRIGGERS_PLACEHOLDER_XXX',
                            'inspect_episode_data_header': 'XXX_INSPECT_EPISODE_DATA_HEADER_PLACEHOLDER_XXX',
                            'inspect_episode_data_body': 'XXX_INSPECT_EPISODE_DATA_BODY_PLACEHOLDER_XXX',
                            'inspect_episode_data_trigger': 'XXX_INSPECT_EPISODE_DATA_TRIGGERS_PLACEHOLDER_XXX',
                            'inspect_fragment_header': 'XXX_INSPECT_FRAGMENT_HEADER_PLACEHOLDER_XXX',
                            'inspect_fragment_body': 'XXX_INSPECT_FRAGMENT_BODY_PLACEHOLDER_XXX',
                            'inspect_fragment_trigger': 'XXX_INSPECT_FRAGMENT_TRIGGERS_PLACEHOLDER_XXX',
                            'set_fragment_header': 'XXX_SET_FRAGMENT_HEADER_PLACEHOLDER_XXX',
                            'set_fragment_body': 'XXX_SET_FRAGMENT_BODY_PLACEHOLDER_XXX',
                            'set_fragment_trigger': 'XXX_SET_FRAGMENT_TRIGGERS_PLACEHOLDER_XXX'}

        # assert that all expected placeholder are found within the xml template
        for key, val in replacement_dict.items():
            try:
                assert re.findall(val, tmp_xml_str) != []
            except AssertionError as e:
                print('\n\n')
                print('#' * 100)
                print(tmp_xml_str)
                print('#' * 100)
                print('\n\n')
                print(f'NOT FOUND:  {key=}, {val=}')
                print('#' * 100)
                print('\n\n')
                raise AssertionError(e)

        # assert that all placeholders found within the xml template are accounted for in replacement_dict values
        for placeholder in re.findall(r'XXX_.+?_XXX', tmp_xml_str):
            try:
                assert placeholder in replacement_dict.values()
            except AssertionError as e:
                print('\n\n')
                print('#' * 100)
                print(tmp_xml_str)
                print('\n\n')
                print('#' * 100)
                print(f'NOT FOUND: {placeholder}')
                raise AssertionError(e)

        # replace placeholder strings
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['variable_declaration'],
                                          self.return_variable_declaration_str())
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['index_body'],
                                          '<!-- index_body -->')
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['index_trigger'],
                                          '<!-- index_trigger-->')

        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_episode_index_body'],
                                          tmp_question_open_episode_index_str)
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_episode_index_trigger'],
                                          '<!-- set_episode_index_trigger-->')

        tmp_xml_str = tmp_xml_str.replace(replacement_dict['reset_json_array_body'],
                                          '<!-- reset_variables_body-->')
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['reset_json_array_trigger'],
                                          self.reset_whole_json())

        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_episode_data_body'],
                                          self.return_all_qml_code())
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_episode_data_trigger'],
                                          self.return_json_load() + self.return_json_save())

        tmp_xml_str = tmp_xml_str.replace(replacement_dict['inspect_episode_data_header'],
                                          self.return_debug_info())
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['inspect_episode_data_body'],
                                          '<!-- inspect_episode_data_body-->')
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['inspect_episode_data_trigger'],
                                          self.return_json_load() + self.return_json_save())

        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_fragment_header'],
                                          '<!-- set_fragment_header -->')
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_fragment_body'],
                                          self.return_fragment_variable_qml_edit_code())
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['set_fragment_trigger'],
                                          '<!-- set_fragment_trigger -->')

        tmp_xml_str = tmp_xml_str.replace(replacement_dict['inspect_fragment_header'],
                                          '<!-- inspect_fragment_header -->')
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['inspect_fragment_body'],
                                          '<!-- inspect_fragment_body-->')
        tmp_xml_str = tmp_xml_str.replace(replacement_dict['inspect_fragment_trigger'],
                                          '<!-- inspect_fragment_trigger -->')

        try:
            assert re.findall(r'XXX_.+?_XXX', tmp_xml_str) == []
        except AssertionError as e:
            print(tmp_xml_str)
            print('\n\n')
            print('#' * 100)
            print('\n\n')
            print(re.findall(r'XXX_.+?_XXX', tmp_xml_str))
            raise AssertionError(e)

        output_file = Path(os.path.abspath(''), 'output', 'questionnaire.xml')
        output_file.write_text(data=tmp_xml_str, encoding='utf-8')

    def print_variable_declaration_str(self) -> None:
        print(self.return_variable_declaration_str())

    def return_variable_declaration_str(self) -> str:
        tmp_variable_declaration_str = '        <zofar:variable name="episode_index" type="string"/>\n'

        # make sure list of fragment variables is up to date
        self.create_list_of_fragment_variables_names()

        for fragment_variable_name in self.list_of_fragment_variables_names:
            tmp_variable_declaration_str += f'        <zofar:variable name="{fragment_variable_name}" type="string"/>\n'

        for question_generator_object in self.list_of_question_qml_generator_objects:
            assert isinstance(question_generator_object, Question_QML_generator)
            question_generator_object.create_question_qml()
            tmp_variable_declaration_str += question_generator_object.variable_declaration_string

        return tmp_variable_declaration_str

    def create_list_of_fragment_variables_names(self) -> None:
        self.list_of_fragment_variables_names = []

        zfill_length = len(str(self.number_of_fragment_variables))

        for i in range(self.number_of_fragment_variables):
            self.list_of_fragment_variables_names.append(
                f'{self.fragment_variable_name_stem}{str(i + 1).zfill(zfill_length)}')

    def add_question_qml_generator(self, qml_generator_object: Question_QML_generator) -> None:
        self.list_of_question_qml_generator_objects.append(qml_generator_object)

    def return_all_qml_code(self) -> str:
        tmp_output_str = ''
        for question_qml_generator_object in self.list_of_question_qml_generator_objects:
            assert isinstance(question_qml_generator_object, Question_QML_generator)
            question_qml_generator_object.create_question_qml()
            tmp_output_str += question_qml_generator_object.generated_qml_string
        return tmp_output_str

    def print_all_qml_code(self) -> None:
        print(self.return_all_qml_code())

    def print_json_load(self) -> None:
        print(self.return_json_load())

    def return_debug_info(self) -> str:
        tmp_debug_info_str = ''
        tmp_debug_info_str += f"""			<zofar:title container="true" uid="t1">
        				episode_index: #{{episode_index.value}} 
        				#{{layout.BREAK}}
                        whole json array:
				        #{{zofar.str2jsonArr(zofar.defrac(zofar.list({','.join(self.list_of_fragment_variables_names)})))}}
				        #{{layout.BREAK}}
			        </zofar:title>\n\n"""
        return tmp_debug_info_str

    def return_json_load(self) -> str:
        # make sure that the list of fragment variable names is up to date
        self.create_list_of_fragment_variables_names()

        self.json_function_code_load = ""
        self.json_function_code_load += """			<zofar:action command="zofar.nothing()" onExit="false">\n"""
        self.json_function_code_load += """				<!-- reset page variables -->\n"""
        self.json_function_code_load += """				<!-- initialize empty list -->\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.assign('toReset',zofar.list())" />\n"""
        self.json_function_code_load += """				\n"""
        self.json_function_code_load += """				<!-- add page variables one after another to the list -->\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="toReset.add('v_startmonth')" />\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="toReset.add('v_startyear')" />\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="toReset.add('v_endmonth')" />\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="toReset.add('v_endyear')" />\n"""
        for qml_generator_object in self.list_of_question_qml_generator_objects:
            assert isinstance(qml_generator_object, Question_QML_generator)
            for variable_name in qml_generator_object.list_of_varnames:
                self.json_function_code_load += f"""				<zofar:scriptItem value="toReset.add('{variable_name}')" />\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += """				<!-- reset all variables stored in list -->\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.resetVars(toReset)" />\n"""
        self.json_function_code_load += """			</zofar:action>\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += """			<!-- BAUKASTEN: BASIC page setup within loop when LOADING page -->\n"""
        self.json_function_code_load += """			<zofar:action command="zofar.nothing()" onExit="false">\n"""
        self.json_function_code_load += """				<!-- ToDo: make generic zofar function from those two commands -->\n"""
        self.json_function_code_load += """				<!-- generic json setup - load whole json array (all episodes) -->\n"""
        self.json_function_code_load += f"""				<zofar:scriptItem value="zofar.assign('defrac',zofar.str2jsonArr(zofar.defrac(zofar.list({','.join(self.list_of_fragment_variables_names)}))))" />\n"""
        self.json_function_code_load += """				<!-- load specific episode json object from json array (by episode index) -->\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.assign('episodeObj',zofar.getOrCreateJson(defrac,zofar.toInteger(episode_index.value))) " />\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += """				<!-- page-specific -->\n"""
        self.json_function_code_load += """				<!-- initiales variables (according to page qml) -->\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.assign('monthMap',zofar.map('1=ao1,2=ao2,3=ao3,4=ao4,5=ao5,6=ao6,7=ao7,8=ao8,9=ao9,10=ao10,11=ao11,12=ao12'))" />\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.assign('yearMap',zofar.map('2018=ao1,2019=ao2,2020=ao3,2021=ao4,2022=ao5,2023=ao6,2024=ao7'))" />\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += """				<!-- <zofar:scriptItem value="zofar.assign('startDate',zofar.getJsonProperty(episodeObj,'startDate')) -->" />\n"""
        self.json_function_code_load += """				<!-- <zofar:scriptItem value="zofar.assign('endDate',zofar.getJsonProperty(episodeObj,'endDate')) -->" />\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += "\n"
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.assign('toLoad',zofar.list())" />\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += "\n"
        for qml_generator_object in self.list_of_question_qml_generator_objects:
            assert isinstance(qml_generator_object, Question_QML_generator)
            for variable_name in qml_generator_object.list_of_varnames:
                self.json_function_code_load += f"""				<zofar:scriptItem value="toLoad.add('{variable_name}')" />\n"""
        self.json_function_code_load += "\n"
        self.json_function_code_load += """				<!-- load all values from episodeObj -->\n"""
        self.json_function_code_load += """				<zofar:scriptItem value="zofar.getJsonProperties(episodeObj,toLoad)" />\n"""
        self.json_function_code_load += """			</zofar:action>\n"""
        self.json_function_code_load += "\n\n"

        return self.json_function_code_load

    def print_json_save(self) -> None:
        print(self.return_json_save())

    def return_json_save(self) -> str:
        # make sure that the list of fragment variable names is up to date
        self.create_list_of_fragment_variables_names()

        tmp_json_function_code_save = "\n"
        tmp_json_function_code_save += """			<!-- BAUKASTEN: BASIC page setup within loop when EXITING page -->\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """			<!-- last command: fragment json object into several variables -->\n"""
        tmp_json_function_code_save += """			<zofar:action\n"""
        tmp_json_function_code_save += f"""				command="zofar.frac(zofar.list({','.join(self.list_of_fragment_variables_names)}),zofar.jsonArr2str(defrac))"\n"""
        tmp_json_function_code_save += """				onExit="true">\n"""
        tmp_json_function_code_save += """				<!-- generic json setup -->\n"""
        tmp_json_function_code_save += """				<zofar:scriptItem\n"""
        tmp_json_function_code_save += f"""					value="zofar.assign('defrac',zofar.str2jsonArr(zofar.defrac(zofar.list({','.join(self.list_of_fragment_variables_names)}))))" />\n"""
        tmp_json_function_code_save += """				<zofar:scriptItem\n"""
        tmp_json_function_code_save += """					value="zofar.assign('episodeObj',zofar.getOrCreateJson(defrac,zofar.toInteger(episode_index.value))) " />\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """				<!--  initialize a map of variables to write to DB -->\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """				<zofar:scriptItem value="zofar.assign('toPersist',zofar.map())" />\n"""
        tmp_json_function_code_save += """					<!-- add variablenames and values to save to DB -->\n"""
        tmp_json_function_code_save += """						<!-- Syntax: toPersist.put('VARIABLENAME',VALUE) -->\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """					<!-- !!Important!! for SC to use valueID instead of Value -->\n"""
        tmp_json_function_code_save += """						<!-- Syntax: toPersist.put('VARIABLENAME',VARIABLENAME.valueId) -->\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """					<!-- all other variables: use value -->\n"""
        tmp_json_function_code_save += """						<!-- Syntax: toPersist.put('VARIABLENAME',VARIABLENAME.value) -->\n"""
        for qml_generator_object in self.list_of_question_qml_generator_objects:
            assert isinstance(qml_generator_object, Question_QML_generator)
            for variable_name in qml_generator_object.list_of_varnames:
                tmp_json_function_code_save += f"""				<zofar:scriptItem value="toPersist.put('{variable_name}',{variable_name}.value)" />\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """				<!-- write all values to episodeObj (still in RAM) -->\n"""
        tmp_json_function_code_save += """				<zofar:scriptItem value="zofar.setJsonProperties('episodeObj',episodeObj,toPersist)" />\n"""
        tmp_json_function_code_save += "\n"
        tmp_json_function_code_save += """				<!-- generic json setup -->\n"""
        tmp_json_function_code_save += """				<!-- save episode object into json array to DB -->\n"""
        tmp_json_function_code_save += """				<zofar:scriptItem value="zofar.assign('defrac',zofar.addOrReplaceJson(defrac,episodeObj,zofar.toInteger(episode_index.value)))" />\n"""
        tmp_json_function_code_save += """			</zofar:action>\n"""
        tmp_json_function_code_save += "\n\n"

        return tmp_json_function_code_save


