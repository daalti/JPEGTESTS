#ifndef DUNE_COPY_SPICE_COPYCONTROLLER_H
#define DUNE_COPY_SPICE_COPYCONTROLLER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppController.h
 * @date   Tue, 17 Feb 2020 13:22:31 +0530
 * @brief  Controller for Copy for Lifestyle Experience
 *
 * (C) Copyright 2020 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ISpiceController.h"
namespace dune { namespace copy { namespace spice {
using namespace dune::spice::core;

class CopyAppController : public ISpiceController
{
    Q_OBJECT
  public:
    /**
     * @brief CopyAppController Constructor.
     */
    explicit CopyAppController(IApplicationEngine *applicationEngine, QObject *parent = nullptr);

    /**
     * Destructor.
     */
    virtual ~CopyAppController();
  public slots:
    void    copyInitialize();
    void    startCopy();
    quint32 getDefaultCopies();
    void    incrementCopies();
    void    decrementCopies();
    void    cancelCopy();

  private:
    quint32 noOfCopies_;
};

}}}     // namespace dune::copy::spice
#endif  // DUNE_COPY_SPICE_COPYCONTROLLER_H
