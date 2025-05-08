from setuptools import setup, find_packages

setup(
    name="index_codebase_tool",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "chromadb",
        "sentence-transformers",
        "huggingface-hub",
        "streamlit"
    ],
    entry_points={
        "console_scripts": [
            "index-codebase=index_codebase_tool.cli:main",
            "code-search-cli=index_codebase_tool.search_cli:main",
            "code-search-gui=index_codebase_tool.search_gui:main"
        ]
    },
    author="あなたの名前",
    description="コードベースをChromaベクトルDBにインデックス化し、検索するCLIツール",
    python_requires=">=3.9"
)
