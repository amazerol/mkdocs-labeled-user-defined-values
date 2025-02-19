from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class LabeledUserDefinedValues(BasePlugin):

    config_scheme = (
        ('keywords', config_options.Type(dict)),
        ('input-placeholder', config_options.Type(str, default='{{{user-defined-values}}}'))
    )

    def on_config(self, config, **kwards):
        self.keywords = {}

        # Sanatise all keywords to be Dictionary. By default MkDocs assigns None as a value for Keys if they are empty
        for key, value in self.config['keywords'].items():
            self.keywords[key] = value if isinstance(value, dict) else {}
        

        self.categories = [key for key, value in self.keywords.items()]
        self.placeholdered_categories = [self.config['input-placeholder'].strip("}}}") + "." + cat + "}}}" for cat in self.categories]


        return config

    def on_post_page(self, output_content, page, config):
        data_tag = 'data-bind-user-defined-values'            

        asked_cat = None
        for asked_placeholder in self.placeholdered_categories:
            if asked_placeholder in output_content:
                asked_cat: str = asked_placeholder.strip("}}}").strip("{{{").split(".")[1]

        mem_keywords = self.keywords


        if asked_cat is not None:
            try:
                self.keywords = self.keywords.pop(asked_cat)
            except: pass

        # Wrap keyword with span and data tag
        for keyword in self.keywords:
            output_content = output_content.replace(keyword, f'<span {data_tag}="{keyword}">{keyword}</span>')

        # Embed binding javascript
        input_boxes = '''
        <style>
            label.user-defined-values {
                width: 30%
            }

            input.user-defined-values[type=text] {
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
                border: 1px solid black;
                display: inline-block;
            }
        </style>
        '''

        for keyword, values in self.keywords.items():
            javascript_variable_name = keyword.lower().replace("-", "_")
            label = keyword
            placeholder = ''

            if values:
                label = values.get('label', label)
                placeholder = values.get('placeholder', placeholder)

            input_boxes += f'''
                <label class="user-defined-values" for="{keyword}">{label}</label>
                <input class="user-defined-values" type="text" placeholder="{placeholder}" id="{keyword}" />
                <script>
                    const {javascript_variable_name} = document.getElementById('{keyword}');
                    {javascript_variable_name}.value = window.localStorage.getItem('{keyword}');
                    {javascript_variable_name}.oninput = function(e) {{
                        const value = e.target.value;
                        window.localStorage.setItem('{keyword}', value);
                        document.querySelectorAll('[{data_tag}="{keyword}"]').forEach(function(element, _) {{
                            if (value == '') {{
                                element.innerHTML = '{keyword}';
                            }} else {{
                                element.innerHTML = value;
                            }}
                        }});
                    }};
                </script>
            '''
        if asked_cat is not None:
            output_content = output_content.replace(self.config['input-placeholder'].strip("}}}") + "." + asked_cat + "}}}", input_boxes)
        else:
            output_content = output_content.replace(self.config['input-placeholder'], input_boxes)

        self.keywords = mem_keywords

        return output_content
