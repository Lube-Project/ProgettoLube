import * as React from 'react';
interface IProps {
    value: number;
    onChange: Function;
    id?: string;
    name?: string;
    defaultValue?: string;
    start?: number;
    end?: number;
    reverse?: boolean;
    required?: boolean;
    disabled?: boolean;
    classes?: string;
    optionClasses?: string;
}
interface IState {
}
export declare class YearPicker extends React.Component<IProps, IState> {
    renderYearOptions: () => JSX.Element[];
    handleSelectionChange: (e: any) => any;
    render: () => JSX.Element;
}
export {};
