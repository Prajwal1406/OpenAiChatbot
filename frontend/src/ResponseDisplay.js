import React from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coy } from "react-syntax-highlighter/dist/esm/styles/prism";
import remarkGfm from "remark-gfm";
import "./App.css";

const ResponseDisplay = ({ response }) => {
  const renderContent = (content) => {
    const codeRegex = /```(.*?)```/gs;
    const parts = content.split(codeRegex);

    return parts.map((part, index) => {
      if (index % 2 === 1) {
        const language = part.split("\n")[0];
        const code = part.replace(`${language}\n`, "");
        return (
          <SyntaxHighlighter key={index} language={language} style={coy}>
            {code}
          </SyntaxHighlighter>
        );
      } else {
        return (
          <p key={index}>
            <ReactMarkdown
              children={response}
              remarkPlugins={[remarkGfm]}
              components={part}
            />
          </p>
        );
      }
    });
  };

  return <div className="response-display">{renderContent(response)}</div>;
};

export default ResponseDisplay;
