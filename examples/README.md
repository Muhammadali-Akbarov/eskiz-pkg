# Examples for eskiz-pkg

This directory contains example scripts demonstrating how to use the eskiz-pkg library.

## Synchronous Client Example

The `sync_example.py` file demonstrates how to use the synchronous client to:

- Send SMS messages
- Send batch SMS messages
- Check balance
- Get message status

To run the example:

```bash
python sync_example.py
```

Make sure to replace the placeholder credentials with your actual Eskiz.uz credentials.

## Asynchronous Client Example

The `async_example.py` file demonstrates how to use the asynchronous client to:

- Send SMS messages
- Send batch SMS messages
- Check balance

To run the example:

```bash
python async_example.py
```

Make sure to install the async dependencies:

```bash
pip install "eskiz-pkg[async]"
```

And replace the placeholder credentials with your actual Eskiz.uz credentials.
