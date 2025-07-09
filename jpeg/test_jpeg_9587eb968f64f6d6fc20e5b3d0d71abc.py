import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PostScript high value test using **9587eb968f64f6d6fc20e5b3d0d71abc.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:9587eb968f64f6d6fc20e5b3d0d71abc.jpg=18f25bed0d24c7ed1203c867676b1d33903edcf6643c77989a31a85721f88357
    +test_classification:System
    +name:test_jpeg_9587eb968f64f6d6fc20e5b3d0d71abc
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_9587eb968f64f6d6fc20e5b3d0d71abc
        +guid:16240742-513d-4f39-8805-0968435a5f2d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_9587eb968f64f6d6fc20e5b3d0d71abc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('18f25bed0d24c7ed1203c867676b1d33903edcf6643c77989a31a85721f88357')
    outputsaver.save_output()
