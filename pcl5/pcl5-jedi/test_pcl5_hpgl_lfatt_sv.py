import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sv.obj=fd18686dc36aa3f1fc807f5eacf0ed57288b80eb9dd780296ab52b2b0862f2a4
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_sv
    +test:
        +title: test_pcl5_hpgl_lfatt_sv
        +guid:831ae418-961b-451f-813c-7ee0aabe2a88
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_sv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fd18686dc36aa3f1fc807f5eacf0ed57288b80eb9dd780296ab52b2b0862f2a4', timeout=600)
    outputsaver.save_output()
