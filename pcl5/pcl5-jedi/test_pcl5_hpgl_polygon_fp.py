import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fp.obj=64814422af13d76a94676ac7c1cc33830655c3bcc84a85b450827f88eca56760
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_fp
    +test:
        +title: test_pcl5_hpgl_polygon_fp
        +guid:569c5895-1d27-4ec5-accd-3071ae4bd241
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_fp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('64814422af13d76a94676ac7c1cc33830655c3bcc84a85b450827f88eca56760', timeout=600)
    outputsaver.save_output()
