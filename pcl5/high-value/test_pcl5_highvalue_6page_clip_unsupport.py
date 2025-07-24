import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_clip_unsupport.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-clip_unsupport.obj=39fca8c23dd99fc36d1d00c28f8f7268bd924461988ecf580160addfbf42db75
    +test_classification:System
    +name: test_pcl5_highvalue_6page_clip_unsupport
    +test:
        +title: test_pcl5_highvalue_6page_clip_unsupport
        +guid:77c82f7f-4c17-4395-8bca-83291f862833
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

def test_pcl5_highvalue_6page_clip_unsupport(setup_teardown, printjob, outputsaver):
    printjob.print_verify('39fca8c23dd99fc36d1d00c28f8f7268bd924461988ecf580160addfbf42db75')
    outputsaver.save_output()
