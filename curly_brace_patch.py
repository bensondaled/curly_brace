from matplotlib.patches import PathPatch, Path
import numpy as np

def CurlyBrace(x, y, width=1/8, height=1., curliness=1/np.e, pointing='left', **patch_kw):
    '''Create a matplotlib patch corresponding to a curly brace (i.e. this thing: "{")

    Parameters
    ----------
    x : float
        x position of left edge of patch
    y : float
        y position of bottom edge of patch
    width : float
        horizontal span of patch
    height : float
        vertical span of patch
    curliness : float
        positive value indicating extent of curliness; default (1/e) tends to look nice
    pointing : str
        direction in which the curly brace points (currently supports 'left' and 'right')
    **patch_kw : any keyword args accepted by matplotlib's Patch

    Returns
    -------
    matplotlib PathPatch corresponding to curly brace
    
    Notes
    -----
    It is useful to supply the `transform` parameter to specify the coordinate system for the Patch.

    To add to Axes `ax`:
    cb = CurlyBrace(x, y)
    ax.add_artist(cb)

    This has been written as a function that returns a Patch because I saw no use in making it a class, though one could extend matplotlib's Patch as an alternate implementation.
    
    Thanks to:
    https://graphicdesign.stackexchange.com/questions/86334/inkscape-easy-way-to-create-curly-brace-bracket
    http://www.inkscapeforum.com/viewtopic.php?t=11228
    https://css-tricks.com/svg-path-syntax-illustrated-guide/
    https://matplotlib.org/users/path_tutorial.html

    Ben Deverett, 2018.


    Examples
    --------
    >>>from curly_brace_patch import CurlyBrace
    >>>import matplotlib.pyplot as pl
    >>>fig,ax = pl.subplots()
    >>>brace = CurlyBrace(x=.4, y=.2, width=.2, height=.6, pointing='right', transform=ax.transAxes, color='magenta')
    >>>ax.add_artist(brace)

    '''

    verts = np.array([
           [width,0],
           [0,0],
           [width, curliness],
           [0,.5],
           [width, 1-curliness],
           [0,1],
           [width,1]
           ])
    
    if pointing == 'left':
        pass
    elif pointing == 'right':
        verts[:,0] = width - verts[:,0]

    verts[:,1] *= height
    
    verts[:,0] += x
    verts[:,1] += y

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]

    path = Path(verts, codes)

    # convert `color` parameter to `edgecolor`, since that's the assumed intention
    patch_kw['edgecolor'] = patch_kw.pop('color', 'black')

    pp = PathPatch(path, facecolor='none', **patch_kw) 
    return pp

if __name__ == '__main__':
    
    import matplotlib.pyplot as pl
    fig,ax = pl.subplots()
    
    for side,point in enumerate(['right','left']):
        for i,(w,h,c) in enumerate(zip(
                np.linspace(.1,.18,4), 
                np.linspace(.95,.5,4),
                np.linspace(.1,.5,4))):
            x = i*.1 if side==0 else 1-i*.1-w
            lw = 3*i+1
            col = pl.cm.plasma(side/2+i/8)
            brace = CurlyBrace(x=x, y=(1-h)/2, width=w, height=h, lw=lw,
                    curliness=c, pointing=point, color=col)
            ax.add_artist(brace)
    ax.axis('off')
