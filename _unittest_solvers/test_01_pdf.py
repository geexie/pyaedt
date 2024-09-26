import os

from _unittest_solvers.conftest import desktop_version
from _unittest_solvers.conftest import local_path
import pytest

from ansys.aedt.core import Circuit
from ansys.aedt.core.visualization.post.compliance import VirtualCompliance
from ansys.aedt.core.visualization.plot.pdf import AnsysReport

tol = 1e-12
test_project_name = "ANSYS-HSD_V1_0_test"
test_subfolder = "T01"


@pytest.fixture(scope="class")
def aedtapp(add_app):
    app = add_app(test_project_name, application=Circuit, subfolder=os.path.join(test_subfolder, "compliance"))
    return app


class TestClass(object):
    def test_create_pdf(self, local_scratch):
        report = AnsysReport(design_name="Design1", project_name="Coaxial")
        report.aedt_version = desktop_version
        assert "AnsysTemplate" in report.template_name
        report.template_name = "AnsysTemplate"
        assert report.project_name == "Coaxial"
        report.project_name = "Coaxial1"
        assert report.project_name == "Coaxial1"
        assert report.design_name == "Design1"
        report.design_name = "Design2"
        assert report.design_name == "Design2"
        report.create()
        report.add_section()
        report.add_chapter("Chapter 1")
        report.add_sub_chapter("C1")
        report.add_text("ciao")
        report.add_text("hola", True, True)
        report.add_empty_line(2)
        report.add_page_break()
        report.add_image(os.path.join(local_path, "example_models", test_subfolder, "Coax_HFSS.jpg"), "Coaxial Cable")
        report.add_section(portrait=False, page_format="a3")
        report.add_table("MyTable", [["x", "y"], ["0", "1"], ["2", "3"], ["10", "20"]])
        report.add_section()
        report.add_chart([0, 1, 2, 3, 4, 5], [10, 20, 4, 30, 40, 12], "Freq", "Val", "MyTable")
        report.add_toc()
        assert os.path.exists(report.save_pdf(local_scratch.path, "my_firstpdf.pdf"))

    def test_virtual_compliance(self, local_scratch, aedtapp):
        template = os.path.join(
            local_path, "example_models", test_subfolder, "compliance", "general_compliance_template.json"
        )
        template = local_scratch.copyfile(template)
        local_scratch.copyfile(
            os.path.join(local_path, "example_models", test_subfolder, "compliance", "ContourEyeDiagram_Custom.json")
        )
        local_scratch.copyfile(
            os.path.join(local_path, "example_models", test_subfolder, "compliance", "spisim_erl.cfg")
        )
        local_scratch.copyfile(
            os.path.join(local_path, "example_models", test_subfolder, "compliance", "Sparameter_Custom.json")
        )
        local_scratch.copyfile(
            os.path.join(local_path, "example_models", test_subfolder, "compliance", "Sparameter_Insertion_Custom.json")
        )
        local_scratch.copyfile(
            os.path.join(
                local_path, "example_models", test_subfolder, "compliance", "StatisticalEyeDiagram_Custom.json"
            )
        )
        local_scratch.copyfile(
            os.path.join(local_path, "example_models", test_subfolder, "compliance", "EyeDiagram_Custom.json")
        )

        import json

        with open(template, "r+") as f:
            data = json.load(f)
            data["general"]["project"] = os.path.join(aedtapp.project_path, aedtapp.project_name + ".aedt")
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        v = VirtualCompliance(aedtapp.desktop_class, template)
        assert v.create_compliance_report()

    def test_spisim_raw_read(self, local_scratch):
        from ansys.aedt.core.visualization.post.spisim import SpiSimRawRead

        raw_file = os.path.join(local_path, "example_models", test_subfolder, "SerDes_Demo_02_Thru.s4p_ERL.raw")
        raw_file = local_scratch.copyfile(raw_file)

        raw_file = SpiSimRawRead(raw_file)
        assert raw_file.get_raw_property()
        assert len(raw_file.get_raw_property("Variables"))
        assert raw_file.trace_names
        assert len(raw_file["time"])
        assert len(raw_file.get_trace(0))
        assert len(raw_file.get_wave(raw_file.trace_names[0])) == len(raw_file.get_axis())
        assert raw_file.__len__() > 0
