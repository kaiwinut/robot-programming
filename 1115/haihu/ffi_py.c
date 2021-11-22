// ffi_py.c
#include <Python.h>
#include <stdio.h>
#include <math.h>

static PyObject * sinc(PyObject *self, PyObject *args)
{
  double d;

  if (!PyArg_ParseTuple(args, "d", &d))
    return NULL;
  d = sin(d)/d;
  return Py_BuildValue("d", d);
}

static PyObject *
hello(PyObject *self, PyObject *args)
{
  const char *str;

  if (!PyArg_ParseTuple(args, "s", &str))
    return NULL;
  fprintf(stdout, "hello %s\n", str);
  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef Methods[] =
  {
   {"sinc",  sinc, METH_VARARGS,"Return sin(x)/x"},
   {"hello",  hello, METH_VARARGS,"Print hello world"},
   {NULL, NULL, 0, NULL}        /* Sentinel */
  };

PyMODINIT_FUNC
initffi_py(void)
{
  (void)Py_InitModule("ffi_py", Methods);
}

#if 0// for python3
static PyMethodDef Methods[] =
  {
   {"sinc",  sinc, METH_VARARGS,"Return sin(x)/x"},
   {"hello",  hello, METH_VARARGS,"Print hello world"},
   {NULL, NULL, 0, NULL}        /* Sentinel */
  };

static struct PyModuleDef Module =
  {
   PyModuleDef_HEAD_INIT,
   "ffi_py",   /* name of module */
   NULL,       /* module documentation, may be NULL */
   -1,         /* size of per-interpreter state of the module,
		  or -1 if the module keeps state in global variables. */
   Methods
};
PyMODINIT_FUNC
PyInit_ffi_py(void)
{
  PyObject *m;

  m = PyModule_Create(&Module);
  if (m == NULL)
    return NULL;

  return m;
}
#endif
