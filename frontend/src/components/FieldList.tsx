interface FieldListProps {
    title: string;
    items: string[];
    isLinkList?: boolean;
}

const FieldList: React.FC<FieldListProps> = ({ title, items, isLinkList = true }) => {
    if (items.length === 0) return null;

    return (
        <p className="mb-2">
            <strong>{title}:</strong>{" "}
            {isLinkList ? (
                items.map((item, index) => (
                    <a key={index} href={item} className="link-primary me-2">
                        {decodeURIComponent(item).split("/").pop()}
                    </a>
                ))
            ) : (
                <span>
                    {items.map((item, index) => (
                        <code className="border border-secondary rounded px-2 py-0.5 m-2" key={index}>
                            {item}
                        </code>
                    ))}
                </span>
            )}
        </p>
    );
};

export default FieldList;