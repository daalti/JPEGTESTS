import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_tgen_ac_10.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-tgen_ac_10.obj=3eaf6af0ecdf85582d5e0159ca90aa86dee0bf08e115fb125f629eb6bdd6a7c3
    +test_classification:System
    +name: test_pcl5_highvalue_1page_tgen_ac_10
    +test:
        +title: test_pcl5_highvalue_1page_tgen_ac_10
        +guid:56ca5378-6447-4441-ad74-de9382378f34
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

def test_pcl5_highvalue_1page_tgen_ac_10(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3eaf6af0ecdf85582d5e0159ca90aa86dee0bf08e115fb125f629eb6bdd6a7c3', timeout=600)
    outputsaver.save_output()
