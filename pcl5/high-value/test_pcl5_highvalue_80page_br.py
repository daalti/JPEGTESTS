import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 80Page_br.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:80Page-br.obj=bbea5b470d255e6e56942a453878e9085fe8eff2a0997cf59f07c7d278c9e8e1
    +test_classification:System
    +name: test_pcl5_highvalue_80page_br
    +test:
        +title: test_pcl5_highvalue_80page_br
        +guid:185db7ff-097e-44bc-9581-836ffeb67e73
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_80page_br(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bbea5b470d255e6e56942a453878e9085fe8eff2a0997cf59f07c7d278c9e8e1', timeout=1500)
    outputsaver.save_output()
