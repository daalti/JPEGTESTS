import pytest
from dunetuf.print.output.intents import Intents, MediaSize, Plex, PlexBinding
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing 2 copies of a PDF file in duplex and 2 copies are printed in duplex
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-188875
    +timeout:150
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_pdf_print_2copies_duplex
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pdf_print_2copies_duplex
        +guid:e36a3c13-52c2-4487-ad01-34421830e4c9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & Duplexer=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_ipp_pdf_print_2copies_duplex(setup_teardown, printjob, outputverifier):

    ipp_test_attribs = {
        'document-format': 'application/pdf',
        'scaling': 'fit', 'sides': 'two-sided-long-edge',
        'copies': '2',
        'multiple-document-handling': 'separate-documents-collated-copies'
    }
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982',timeout = 150)

    outputverifier.save_and_parse_output()
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
