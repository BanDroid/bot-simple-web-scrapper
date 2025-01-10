from bs4 import BeautifulSoup


class BsParser:
    def __init__(self, html_str: str):
        self.document = BeautifulSoup(html_str, "html.parser")
        self.results: list[dict[str, (str | list[str])]] = []

    def process_selector(self, selector: str, attributes: list[str]):
        """
        Process data from given selector.

        Args:
            selector (str): A string containing CSS selector.
            attributes (list[str]): list of attributes that would be extracted.

        Returns:
            list[dict[str, (str | list[str])]]: would return dictionary list.

        Raises:
            ValueError: If elements not found from the given selector.
        """
        # Find elements matching the selector
        elements = self.document.select(selector)
        if not elements:
            raise ValueError("No elements found for the given selector.")

        # Extract attributes for each element
        for element in elements:
            data: dict[str, (str | list[str])] = {}
            for i, attr in enumerate(attributes):
                if attr == "innerText" or attr == "text":
                    data[f"${i+1}"] = element.get_text()
                elif attr == "innerHTML":
                    data[f"${i+1}"] = "".join(str(x) for x in element)
                else:
                    data[f"${i+1}"] = element.get(attr, "")
            self.results.append(data)

    def get_formatted_output(self, template: str):
        # Format the output using the template
        formatted_results = []
        for i, data in enumerate(self.results):
            str_item = template
            for key, val in data.items():
                str_item = str_item.replace(key, str(val))
            formatted_results.append(str_item)
        string_results = "\n".join(formatted_results)
        return BeautifulSoup(string_results, "html.parser").prettify()
