from typing import Annotated

from fastapi import APIRouter, Body, Depends
from utils.utils import connection_db

from schemas import *

