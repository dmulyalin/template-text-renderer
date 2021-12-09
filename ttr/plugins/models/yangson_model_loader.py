"""
Yangson models loader
*********************

**Reference name** ``yangson``

This plugin loads YANG models into yangson DataModel objects.

YANG models must sit within their own directories, each such a directory used to create
JSON library for Yangson to load models from.

Directory name, main YANG model file name and module name must be the same, directory
name used as a reference name for the model.

For example, this is directory tree with YANG models inside::

    |-- Models
        |-- interface
            |-- ietf-inet-types@2013-07-15.yang
            |-- interface.yang
        |-- vrf
            |-- vrf.yang

Above directory structure translated to two models named ``interface`` and ``vrf``, these
names can be used to reference models in data for validation, e.g.::

    - interface: Gi1/1
      description: Customer A
      vid: 100
      ip: 10.0.0.1
      mask: 255.255.255.0
      vrf: cust_a
      device: R1
      template: interfaces.cisco_ios
      model: interface # YANG model name to validate this data item

For reference, YANG model ``Models/interface/interface.yang`` file content is::

    module interface {
        yang-version "1.1";

        namespace "http://ttr/test-1";

        import ietf-inet-types {
        prefix inet;
        }

        typedef ipmask {
        type string {
            pattern '([0-9]{1,3}.){3}[0-9]{1,3}';
        }
        description
            "Pattern to match strings like 255.255.255.0 or 255.0.0.0";
        }

        prefix "ttr";

        leaf interface {
            mandatory true;
            type string;
        }
        leaf template {
            mandatory true;
            type string;
        }
        leaf device {
            mandatory true;
            type string;
        }
        leaf description{
            type string;
        }
        leaf vid {
            type int32;
        }
        leaf ip {
            type inet:ipv4-address;
        }
        leaf mask {
            type ipmask;
        }
        leaf vrf {
            type string;
        }
    }

.. autofunction:: ttr.plugins.models.yangson_model_loader.load
"""
import logging
import json
import os

log = logging.getLogger(__name__)

try:
    from yangson.statement import ModuleParser
    from yangson import DataModel

    HAS_LIBS = True
except ImportError:
    log.debug(
        "ttr.yangson_model_loader: failed to import yangson library, make sure it is installed"
    )
    HAS_LIBS = False


def _module_entry(yfile, modmap, submodmap):
    """
    Add entry for one file containing YANG module text.

    :param yfile: (file) File containing a YANG module or submodule.
    """
    data_kws = [
        "augment",
        "container",
        "leaf",
        "leaf-list",
        "list",
        "rpc",
        "notification",
        "identity",
    ]  # Keywords of statements that contribute nodes to the schema tree
    ytxt = yfile.read()
    mp = ModuleParser(ytxt)
    mst = mp.statement()
    submod = mst.keyword == "submodule"
    import_only = True
    rev = ""
    features = []
    includes = []
    rec = {}
    for sst in mst.substatements:
        if not rev and sst.keyword == "revision":
            rev = sst.argument
        elif import_only and sst.keyword in data_kws:
            import_only = False
        elif sst.keyword == "feature":
            features.append(sst.argument)
        elif submod:
            continue
        elif sst.keyword == "namespace":
            rec["namespace"] = sst.argument
        elif sst.keyword == "include":
            rd = sst.find1("revision-date")
            includes.append((sst.argument, rd.argument if rd else None))
    rec["import-only"] = import_only
    rec["features"] = features
    if submod:
        rec["revision"] = rev
        submodmap[mst.argument] = rec
    else:
        rec["includes"] = includes
        modmap[(mst.argument, rev)] = rec


def _make_library(ydir):
    """
    Make JSON library of YANG modules.

    :param ydir: (str) Name of the directory with YANG (sub)modules.
    """
    modmap = {}  # Dictionary for collecting module data
    submodmap = {}  # Dictionary for collecting submodule data
    for infile in os.listdir(ydir):
        if not infile.endswith(".yang"):
            continue
        with open(
            "{ydir}/{infile}".format(ydir=ydir, infile=infile), "r", encoding="utf-8"
        ) as yf:
            _module_entry(yf, modmap, submodmap)
    marr = []
    for item in modmap:
        yam, mrev = item
        men = {"name": yam, "revision": mrev}
        sarr = []
        mrec = modmap[(yam, mrev)]
        men["namespace"] = mrec["namespace"]
        fts = mrec["features"]
        imp_only = mrec["import-only"]
        for (subm, srev) in mrec["includes"]:
            sen = {"name": subm}
            try:
                srec = submodmap[subm]
            except KeyError:
                log.error(
                    "ttr:yangson_model_loader: Submodule {} not available.".format(subm)
                )
                return 1
            if srev is None or srev == srec["revision"]:
                sen["revision"] = srec["revision"]
            else:
                log.error(
                    "ttr:yangson_model_loader: Submodule {} revision mismatch.".format(
                        subm
                    )
                )
                return 1
            imp_only = imp_only or srec["import-only"]
            fts += srec["features"]
            sarr.append(sen)
        if fts:
            men["feature"] = fts
        if sarr:
            men["submodule"] = sarr
        men["conformance-type"] = "import" if imp_only else "implement"
        marr.append(men)
    res = {"ietf-yang-library:modules-state": {"module-set-id": "", "module": marr}}
    return json.dumps(res, indent=2)


def load(models_dict, models_dir, **kwargs):  # pylint: disable=unused-argument
    """
    Creates JSON-encoded YANG library data [RFC7895] and instantiates data model object out of it.

    :param models_dir: (str) OS path to directory with YANG models modules subdirectories, each
        subdirectory models loaded to form single DataModel and added to models_dict under
        directory name key.
    :param models_dict: (dict) dictionary to store loaded model object at
    :param kwargs: (dict) any additional arguments ignored
    :param return: None
    """
    if not HAS_LIBS:
        raise RuntimeError(
            "ttr:yangson_model_loader: Failed to import yangson library, make sure it is installed."
        )

    # create models one per-directory under models_dir path
    for directory in os.listdir(models_dir):
        if directory in models_dict:
            log.debug(
                "ttr:yangson_module_loader model '{}' already loaded, skipping".format(
                    directory
                )
            )
            continue
        path = os.path.join(models_dir, directory)
        yang_modules_library = _make_library(path)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                "ttr:yangson_module_loader constructed '{}' YANG modules library:\n{}".format(
                    directory, yang_modules_library
                )
            )
        models_dict[directory] = DataModel(yltxt=yang_modules_library, mod_path=[path])
        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                "ttr:yangson_module_loader loaded '{}' YANG model:\n{}".format(
                    directory, models_dict[directory].ascii_tree()
                )
            )
