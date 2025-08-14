
import React, { useState } from 'react';

const MetaChat = ({ title, bodyPlaceholder, inputPlaceholder }: { title: string, bodyPlaceholder: string, inputPlaceholder: string }) => {
    const [input, setInput] = useState<string>('');
    const [response, setResponse] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        setIsLoading(true);
        setResponse('');

        try {
            const res = await fetch("http://localhost:8005/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    prompt: input,
                    tone: "realistic",
                    style: "technical"
                })
            });

            if (!res.ok) {
                throw new Error(`Server error: ${res.status}`);
            }

            const data = await res.json();
            setResponse(data.response || "No valid reply field.");
        } catch (err) {
            console.error(err);
            setResponse("Error: Unable to reach the assistant.");
        } finally {
            setIsLoading(false);
            setInput('');
        }
    };

    return (
        <section id="chat" className="w-full pb-7 pt-1 c-space border-slateGray">
            <div className="max-w-3xl mx-auto flex flex-col gap-6">
                <h2 className="text-white text-3xl font-semibold text-center">{title}</h2>

                <div className="w-full min-h-[150px] bg-cyan-900 border-slateGray rounded-xl p-6 text-white text-lg transition-all duration-200">
                    {response ? (
                        <p>{response}</p>
                    ) : (
                        <p className="italic opacity-60">{bodyPlaceholder}</p>
                    )}
                </div>

                <form onSubmit={handleSubmit} className="flex items-center gap-4">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={inputPlaceholder}
                        className="flex-1 px-4 py-3 rounded-md bg-gray-300 text-black border-slateGray focus:outline-none focus:ring-2 focus:ring-slateGray"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className={`px-6 py-3 bg-gray-500 text-white rounded-md transition-all duration-200 
                                    ${isLoading ? 'opacity-60 cursor-not-allowed' : 'hover:bg-opacity-80'}`}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Sending...' : 'Send'}
                    </button>
                </form>
            </div>
        </section>
    );
};

export default MetaChat;
