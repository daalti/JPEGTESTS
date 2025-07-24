import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 56Page_dic_long.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:56Page-dic_long.obj=68d014ee860fd312b7e5d9b82e33add12eec6d48c365c1235cae0acabec49db3
    +test_classification:System
    +name: test_pcl5_highvalue_56page_dic_long
    +test:
        +title: test_pcl5_highvalue_56page_dic_long
        +guid:3e730fe2-9467-4ab9-8f5d-a9769491c3b4
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

def test_pcl5_highvalue_56page_dic_long(setup_teardown, printjob, outputsaver):
    printjob.print_verify('68d014ee860fd312b7e5d9b82e33add12eec6d48c365c1235cae0acabec49db3', timeout=1500)
    outputsaver.save_output()
