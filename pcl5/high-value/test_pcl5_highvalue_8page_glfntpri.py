import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 8Page_glfntpri.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:8Page-glfntpri.obj=6e5b96caea2a8be0c7a5b91b6a1de1d7ae0f6c299de08a92a1992838b00abf25
    +test_classification:System
    +name: test_pcl5_highvalue_8page_glfntpri
    +test:
        +title: test_pcl5_highvalue_8page_glfntpri
        +guid:2836f0dc-4b61-4880-a590-59743af676ab
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_8page_glfntpri(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6e5b96caea2a8be0c7a5b91b6a1de1d7ae0f6c299de08a92a1992838b00abf25')
    outputsaver.save_output()
