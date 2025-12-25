from __future__ import annotations

import gdsfactory as gf
import klayout

import numpy as np
from collections.abc import Sequence


def reticle(
    size: gf.typings.Size,
    scale: float,
    clearance: float,
    component: gf.Component,
    image_size: gf.typings.Size,
    image_layers: Sequence[gf.typings.LayerSpec],
    geometry_layer: gf.typings.LayerSpec,
) -> Sequence[gf.Component]:
    """Returns a series of reticles populated with given images

    Args:
        size: reticle size (reticle scale)
        scale: reticle scale, reticle scale = scale * image scale
        clearance: minimum clearance between images (reticle scale)
        component: component containing all images
        image_size: size of each image (image scale)
        image_layers: layer numbers of each image
        geometry_layer: reticle polygon layer
    """
    n_x = (size[0] + clearance) // (scale * image_size[0] + clearance)
    n_y = (size[1] + clearance) // (scale * image_size[1] + clearance)
    n_r = int(np.ceil(len(image_layers) / (n_x * n_y)))

    reticles = [gf.Component() for _ in range(n_r)]
    for r in range(n_r):
        for y in range(n_y):
            for x in range(n_x):
                i = x + y * n_x + r * n_x * n_y
                if i >= len(image_layers):
                    break
                image = component.extract(layers=[image_layers[i]]).remap_layers(
                    {image_layers[i]: geometry_layer}
                )
                image.transform(klayout.dbcore.DCplxTrans(mag=scale))
                image_ref = reticles[r] << image
                image_ref.move(
                    (
                        x * (scale * image_size[0] + clearance),
                        y * (scale * image_size[1] + clearance),
                    )
                )
                image_ref.move(
                    (
                        -0.5 * (n_x - 1) * (scale * image_size[0] + clearance),
                        -0.5 * (n_y - 1) * (scale * image_size[1] + clearance),
                    )
                )
        reticles[r].flatten()

    return reticles
