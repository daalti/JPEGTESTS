#ifndef DUNE_COPY_SPICE_COPYSTARTVIEW_H
#define DUNE_COPY_SPICE_COPYSTARTVIEW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyStartView.h
 * @date   Tue, 17 Feb 2020 13:22:31 +0530
 * @brief  Copy Application for Lifestyle Experience
 *
 * (C) Copyright 2020 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include <QObject>

#include "SpiceView.h"
namespace dune { namespace copy { namespace spice {
using namespace dune::spice::core;

class CopyStartView : public SpiceView
{
    Q_OBJECT
  public:
    CopyStartView(SpiceView::ViewPriority priority, ISpiceController* controller, QObject* parent = nullptr);
    ~CopyStartView() {}
  public slots:
    virtual void onActive() override;
};
}}}     // namespace dune::copy::spice
#endif  // DUNE_COPY_SPICE_COPYSTARTVIEW_H
