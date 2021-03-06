#!/usr/bin/env python3

import asyncio

import pytest
from asynctest import patch

from aiospamc import Client
from aiospamc.exceptions import BadResponse, AIOSpamcConnectionFailed
from aiospamc.responses import Response
from aiospamc.requests import Request


@pytest.mark.asyncio
@pytest.mark.usefixtures('connection_refused')
async def test_report_if_spam_connection_refused(spam):
    client = Client(host='localhost')
    with pytest.raises(AIOSpamcConnectionFailed):
        response = await client.report_if_spam(spam)


@pytest.mark.asyncio
@patch('aiospamc.client.Client.send')
async def test_report_if_spam_valid_request(mock_connection, spam):
    client = Client(host='localhost')
    response = await client.report_if_spam(spam)

    request = client.send.call_args[0][0]

    assert isinstance(request, Request)
    assert request.verb == 'REPORT_IFSPAM'
    assert request.body


@pytest.mark.asyncio
async def test_report_if_spam_valid_response(mock_connection, spam):
    client = Client(host='localhost')
    response = await client.report_if_spam(spam)

    assert isinstance(response, Response)


@pytest.mark.asyncio
async def test_report_if_spam_invalid_response(mock_connection, response_invalid, spam):
    mock_connection.side_effect = [response_invalid]

    client = Client(host='localhost')
    with pytest.raises(BadResponse):
        response = await client.report_if_spam(spam)
