# adapted from https://github.com/bugcrowd/HUNT

from bbot.modules.base import BaseModule

hunt_param_dict = {
    "Command Injection": [
        "daemon",
        "host",
        "upload",
        "dir",
        "execute",
        "download",
        "log",
        "ip",
        "cli",
        "cmd",
        "exec",
        "command",
        "func",
        "code",
        "update",
        "shell",
        "eval",
    ],
    "Debug": [
        "access",
        "admin",
        "dbg",
        "debug",
        "edit",
        "grant",
        "test",
        "alter",
        "clone",
        "create",
        "delete",
        "disable",
        "enable",
        "exec",
        "execute",
        "load",
        "make",
        "modify",
        "rename",
        "reset",
        "shell",
        "toggle",
        "adm",
        "root",
        "cfg",
        "config",
    ],
    "Directory Traversal": ["entry", "download", "attachment", "basepath", "path", "file", "source", "dest"],
    "Local File Include": [
        "file",
        "document",
        "folder",
        "root",
        "path",
        "pg",
        "style",
        "pdf",
        "template",
        "php_path",
        "doc",
        "lang",
        "include",
        "img",
        "view",
        "layout",
        "export",
        "log",
        "configFile",
        "stylesheet",
        "configFileUrl",
    ],
    "Insecure Direct Object Reference": [
        "id",
        "user",
        "account",
        "number",
        "order",
        "no",
        "doc",
        "key",
        "email",
        "group",
        "profile",
        "edit",
        "report",
        "docId",
        "accountId",
        "customerId",
        "reportId",
        "jobId",
        "sessionId",
        "api_key",
        "instance",
        "identifier",
        "access",
    ],
    "SQL Injection": [
        "id",
        "" "select",
        "report",
        "role",
        "update",
        "query",
        "user",
        "name",
        "sort",
        "where",
        "search",
        "params",
        "category",
        "process",
        "row",
        "view",
        "table",
        "from",
        "sel",
        "results",
        "sleep",
        "fetch",
        "order",
        "keyword",
        "column",
        "field",
        "delete",
        "string",
        "number",
        "filter",
        "limit",
        "offset",
        "item",
        "input",
        "date",
        "value",
        "orderBy",
        "groupBy",
        "pageNum",
        "pageSize",
        "tag",
        "author",
        "postId",
        "parentId",
        "d",
    ],
    "Server-side Request Forgery": [
        "dest",
        "redirect",
        "uri",
        "path",
        "continue",
        "url",
        "window",
        "next",
        "data",
        "reference",
        "site",
        "html",
        "val",
        "validate",
        "domain",
        "callback",
        "return",
        "page",
        "feed",
        "host",
        "port",
        "to",
        "out",
        "view",
        "dir",
        "show",
        "navigation",
        "open",
        "proxy",
        "target",
        "server",
        "domain",
        "connect",
        "fetch",
        "apiEndpoint",
    ],
    "Server-Side Template Injection": [
        "template",
        "preview",
        "id",
        "view",
        "activity",
        "name",
        "content",
        "redirect",
        "expression",
        "statement",
        "tpl",
        "render",
        "format",
        "engine",
    ],
    "XML external entity injection": [
        "xml",
        "dtd",
        "xsd",
        "xmlDoc",
        "xmlData",
        "entityType",
        "entity",
        "xmlUrl",
        "schema",
        "xmlFile",
        "xmlPath",
        "xmlSource",
        "xmlEndpoint",
        "xslt",
        "xmlConfig",
        "xmlCallback",
        "attributeName",
        "wsdl",
        "xmlDocUrl",
    ],
    "Insecure Cryptography": [
        "encrypted",
        "cipher",
        "iv",
        "checksum",
        "hash",
        "salt",
        "hmac",
        "secret",
        "key",
        "signatureAlgorithm",
        "keyId",
        "sharedSecret",
        "privateKeyId",
        "privateKey",
        "publicKey",
        "publicKeyId",
        "encryptedData",
        "encryptedMessage",
        "encryptedPayload",
        "encryptedFile",
        "cipherText",
        "cipherAlgorithm",
        "keySize",
        "keyPair",
        "keyDerivation",
        "encryptionMethod",
        "decryptionKey",
    ],
    "Unsafe Deserialization": [
        "serialized",
        "object",
        "dataObject",
        "serialization",
        "payload",
        "encoded",
        "marshalled",
        "pickled",
        "jsonData",
        "state",
        "sessionData",
        "cache",
        "tokenData",
        "serializedSession",
        "objectState",
        "jsonDataPayload",
    ],
}


class hunt(BaseModule):
    watched_events = ["HTTP_RESPONSE"]
    produced_events = ["FINDING"]
    flags = ["active", "safe", "web-thorough"]
    meta = {
        "description": "Watch for commonly-exploitable HTTP parameters",
        "created_date": "2022-07-20",
        "author": "@liquidsec",
    }
    # accept all events regardless of scope distance
    scope_distance_modifier = None

    async def handle_event(self, event):
        body = event.data.get("body", "")
        for p in await self.helpers.re.extract_params_html(body):
            for k in hunt_param_dict.keys():
                if p.lower() in hunt_param_dict[k]:
                    description = f"Found potential {k.upper()} parameter [{p}]"
                    data = {"host": str(event.host), "description": description}
                    url = event.data.get("url", "")
                    if url:
                        data["url"] = url
                    await self.emit_event(data, "FINDING", event)
