import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ra_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ra_igm.obj=8cd668fe86241415fc29e62e03dfcecb0233834ad66306bbd18c507e9a9c885a
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ra_igm
    +test:
        +title: test_pcl5_hpgl_polygon_ra_igm
        +guid:6c807d46-1f51-4772-9897-5501d82f0042
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ra_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8cd668fe86241415fc29e62e03dfcecb0233834ad66306bbd18c507e9a9c885a', timeout=600)
    outputsaver.save_output()
